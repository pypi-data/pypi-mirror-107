from __future__ import annotations

import abc
import json
import time
from contextlib import contextmanager
from threading import Thread
from typing import Any, Callable, Dict, Iterator, NamedTuple, Optional

import pika
from pika.connection import Parameters

from rabbitmq_alphamoon.logger import get_logger

LOGGER = get_logger('rabbitmq_alphamoon')


class IQueueConnector(metaclass=abc.ABCMeta):
    @contextmanager
    def open_connection(self) -> Iterator[RabbitMQConnector]:
        pass

    @abc.abstractmethod
    def consume_forever(self, process_message_callback: Callable[[Any, Dict[str, Any]], None]):
        pass

    @abc.abstractmethod
    def publish(self, message: Any) -> None:
        pass

    @property
    @abc.abstractmethod
    def message_count(self) -> int:
        pass


_RabbitMQConnection = NamedTuple(
    '_RabbitMQConnection',
    [
        ('connection', pika.BlockingConnection),
        ('channel', pika.adapters.blocking_connection.BlockingChannel),
        ('queue_declaration', pika.frame.Method),
    ],
)

_DEFAULT = None


class RabbitMQConnector(IQueueConnector):
    def __init__(
        self,
        connection_parameters: Parameters,
        queue: str,
        durable: bool = True,
        exclusive: bool = False,
        auto_delete: bool = False,
        dead_letter_exchange: bool = False,
        requeue_on_consumption_error=_DEFAULT,
    ):
        """
        Set up RabbitMQ connector.

        Important note on `dead_letter_exchange` and `requeue_on_consumption_error`:

            `dead_letter_exchange` causes `dlx_retry_count` incrementation for failed messages.

            `requeue_on_consumption_error` causes messages for which processing failed
            (i.e. message deserialization or processing callback failed) to be requeued again.
            `redelivered` flag will be set to `True` for such messages.

            Using both `dead_letter_exchange` and `requeue_on_consumption_error` may be undesired:
                - rejected messages (processing failed) -> requeued
                  (`redelivered` set to `True`, `dlx_retry_count` not incremented),
                - expired messages -> DLX -> published again
                  (`dlx_retry_count` incremented, `redelivered` set to `False`).

        :param connection_parameters: connection parameters
        :param queue: queue name
        :param durable: whether to store queue on the disk (massages will remain after restarts)
        :param exclusive:
        :param auto_delete: automatically delete queue when disconnected
        :param dead_letter_exchange: whether to set up DLX for failed messages
        :param requeue_on_consumption_error: whether to retry messages if processing failed
        """
        self._connection_parameters = connection_parameters
        self._queue = queue
        self._durable = durable
        self._exclusive = exclusive
        self._auto_delete = auto_delete
        self._dead_letter_exchange = f'dlx.{self._queue}' if dead_letter_exchange else None

        self._requeue = (  # when using DLX, don't requeue failed messages by default
            requeue_on_consumption_error
            if requeue_on_consumption_error is not _DEFAULT
            else not dead_letter_exchange
        )

        self._connection: Optional[_RabbitMQConnection] = None
        self._queue_declaration = None

    def _connect(self):
        LOGGER.debug("Connecting to broker, queue %s", self._queue)
        connection = pika.BlockingConnection(self._connection_parameters)
        channel = connection.channel()
        channel.confirm_delivery()

        queue_arguments = {}
        if self._dead_letter_exchange:
            queue_arguments['x-dead-letter-exchange'] = self._dead_letter_exchange

        queue_declaration = channel.queue_declare(
            queue=self._queue,
            durable=self._durable,
            exclusive=self._exclusive,
            auto_delete=self._auto_delete,
            arguments=queue_arguments,
        )

        if self._dead_letter_exchange:
            channel.exchange_declare(
                exchange=self._dead_letter_exchange,
                durable=self._durable,
            )
            channel.queue_bind(
                exchange=self._dead_letter_exchange,
                routing_key=self._queue,
                queue=self._queue,
            )
            LOGGER.info(
                "Dead letter exchange enabled, exchange %s, queue %s",
                self._dead_letter_exchange,
                self._queue,
            )

        self._connection = _RabbitMQConnection(
            connection=connection,
            channel=channel,
            queue_declaration=queue_declaration,
        )
        LOGGER.info("Connection with broker established, queue %s", self._queue)

    def _assure_connection(self):
        while True:
            try:
                self._connect()
            except pika.exceptions.AMQPConnectionError as error:
                error_type = type(error).__name__  # e.g. 'AMQPConnectionError'
                LOGGER.warning("%s, queue %s: %s, retrying...", error_type, self._queue, error)
                time.sleep(1)
            else:
                break

    def _disconnect(self):
        LOGGER.debug("Disconnecting from broker, queue %s", self._queue)
        self._connection.connection.close()
        self._connection = None
        LOGGER.info("Disconnected from broker, queue %s", self._queue)

    @contextmanager
    def open_connection(self) -> Iterator[RabbitMQConnector]:
        self._assure_connection()
        try:
            yield self  # simplify one-time connector usage, especially when `consume_forever` used
        finally:
            self._disconnect()

    def _get_opened_connection(self) -> _RabbitMQConnection:
        if self._connection is None:
            raise RuntimeError("Connection not opened. Forgot to run in `open_connection` context?")
        return self._connection

    def _reconnect_and_get_opened_connection(self) -> _RabbitMQConnection:
        LOGGER.info("Reconnecting to queue, queue %s", self._queue)
        try:
            self._disconnect()
        except pika.exceptions.AMQPConnectionError as error:
            LOGGER.debug("Ignored disconnection error, queue %s, error %s", self._queue, error)
        else:
            LOGGER.warning("Connection was established, reconnecting anyway, queue %s", self._queue)

        self._assure_connection()
        return self._get_opened_connection()

    def consume_forever(self, process_message_callback: Callable[[Any, Dict[str, Any]], None]):
        connection = self._get_opened_connection()

        def callback_fun(
            channel: pika.channel.Channel,
            deliver: pika.spec.Basic.Deliver,
            properties: pika.BasicProperties,
            body: bytes,
        ):
            tag = deliver.delivery_tag
            LOGGER.info("Received message # %s, queue %s", tag, self._queue)

            def send_ack():
                channel.basic_ack(delivery_tag=tag)
                LOGGER.info("Sent ack for message # %s, queue %s", tag, self._queue)

            def send_reject():
                channel.basic_reject(delivery_tag=tag, requeue=self._requeue)
                LOGGER.info(
                    "Sent reject with requeue=%s for message # %s, queue %s",
                    self._requeue,
                    tag,
                    self._queue,
                )

            def process_fun():
                try:
                    LOGGER.debug("Deserializing body of message # %s, queue %s", tag, self._queue)
                    message = json.loads(body)
                except Exception as error:
                    LOGGER.error(
                        "Deserializing body failed for message of # %s, queue %s, %s: %s",
                        tag,
                        self._queue,
                        type(error).__name__,
                        error,
                    )
                    try:
                        LOGGER.debug("Sending reject for message # %s, queue %s", tag, self._queue)
                        channel.connection.add_callback_threadsafe(send_reject)
                    except pika.exceptions.AMQPError as amqp_error:
                        LOGGER.error(
                            "Sending reject failed for message # %s, queue %s, %s: %s",
                            tag,
                            self._queue,
                            type(amqp_error).__name__,
                            amqp_error,
                        )
                    raise

                info = {}
                if self._requeue:
                    info['redelivered'] = deliver.redelivered
                if self._dead_letter_exchange:
                    x_death_header = (properties.headers or {}).get('x-death', [{}])[0]
                    info['dlx_retry_count'] = x_death_header.get('count', 0)
                    info['dlx_last_fail_reason'] = x_death_header.get('reason')

                try:
                    LOGGER.info("Processing message # %s, queue %s", tag, self._queue)
                    process_message_callback(message, info)
                except Exception as error:
                    LOGGER.error(
                        "Processing message in callback failed for # %s, queue %s, %s: %s",
                        tag,
                        self._queue,
                        type(error).__name__,
                        error,
                    )
                    try:
                        LOGGER.debug("Sending reject for message # %s, queue %s", tag, self._queue)
                        channel.connection.add_callback_threadsafe(send_reject)
                    except pika.exceptions.AMQPError as amqp_error:
                        LOGGER.error(
                            "Sending reject failed for message # %s, queue %s, %s: %s",
                            tag,
                            self._queue,
                            type(amqp_error).__name__,
                            amqp_error,
                        )
                    raise

                try:
                    LOGGER.debug("Sending ack for message # %s, queue %s", tag, self._queue)
                    channel.connection.add_callback_threadsafe(send_ack)
                except pika.exceptions.AMQPError as error:
                    LOGGER.error(
                        "Sending ack failed for message # %s, queue %s, %s: %s",
                        tag,
                        self._queue,
                        type(error).__name__,  # type of an error, e.g. 'ConnectionClosedByBroker'
                        error,
                    )

            # Running the processing in separate thread allow for connection keep-alive as the main
            # thread is not being blocked by the processing.
            Thread(target=process_fun, name=f'message # {tag}, queue {self._queue}').start()

        try:
            while True:
                try:
                    LOGGER.debug("Starting consumption, queue %s", self._queue)
                    connection.channel.basic_qos(prefetch_count=1)  # this limits number of threads
                    connection.channel.basic_consume(
                        queue=self._queue,
                        on_message_callback=callback_fun,
                        auto_ack=False,
                    )
                    connection.channel.start_consuming()
                except KeyboardInterrupt:
                    break
                except pika.exceptions.AMQPConnectionError as error:
                    error_type = type(error).__name__  # e.g. 'ConnectionClosedByBroker'
                    LOGGER.warning("%s, queue %s: %s, retrying...", error_type, self._queue, error)
                    time.sleep(1)
                    connection = self._reconnect_and_get_opened_connection()
                except pika.exceptions.AMQPChannelError as error:
                    error_type = type(error).__name__  # e.g. 'ChannelWrongStateError'
                    LOGGER.error("%s, queue %s: %s, stopping...", error_type, self._queue, error)
                    break
        finally:
            LOGGER.debug("Stopping consumption, queue %s", self._queue)
            connection.channel.stop_consuming()

    def publish(self, message: Any) -> None:
        connection = self._get_opened_connection()
        LOGGER.debug("Serializing message, queue %s", self._queue)
        body = json.dumps(
            message,
            ensure_ascii=False,
            separators=(',', ':'),  # compact encoding
        )

        try:
            LOGGER.debug("Publishing message, queue %s", self._queue)
            connection.channel.basic_publish(
                exchange='',
                routing_key=self._queue,
                body=body.encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,  # persists during restarts
                ),
                mandatory=True,  # ack's when message is received
            )
            LOGGER.info("Published message, queue %s", self._queue)
        except pika.exceptions.UnroutableError as error:
            LOGGER.error("Publishing failed, queue %s, %s", self._queue, error)

    @property
    def message_count(self) -> int:
        connection = self._get_opened_connection()
        return connection.queue_declaration.method.message_count
