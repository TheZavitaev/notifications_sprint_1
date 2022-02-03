import json
import logging
import uuid
from typing import Callable, Optional

import backoff
import pika
from config import config
from models import Event
from pika import channel as pika_channel  # noqa: F401
from pika.adapters.blocking_connection import BlockingChannel

from .abstract import DataSourceAbstract

logger = logging.getLogger(__name__)


TEMPLATE_ID = {
    'common': 2,
    'monthly_personal_statistic': 3
}


class DataSourceRabbitMQ(DataSourceAbstract):
    credentials = pika.PlainCredentials(
        config.rabbit_username,
        config.rabbit_password,
    )
    parameters = pika.ConnectionParameters(
        config.rabbit_host,
        credentials=credentials,
    )

    def __init__(self, worker):
        self.queue = config.rabbit_events_queue_name
        self.connection = self._connect()
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange=config.rabbit_exchange,
            exchange_type=config.rabbit_exchange_type,
            durable=True,
        )
        self.channel.queue_declare(
            queue=config.rabbit_events_queue_name,
            durable=True
        )
        self.worker = worker

        logger.info('Connected to queue.')

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError)
    def _connect(self):
        return pika.BlockingConnection(parameters=self.parameters)

    def decode_data(self, body: bytes) -> Optional[dict]:
        try:
            return json.loads(body)
        except json.decoder.JSONDecodeError as exc:
            logger.exception(exc)
            return None

    def listen_events(self):
        if self.channel:
            self.channel.exchange_declare(
                exchange=config.rabbit_exchange,
                exchange_type=config.rabbit_exchange_type,
                durable=True
            )

            self.channel.queue_declare(queue=self.queue, durable=True)
            self.channel.queue_bind(
                exchange=config.rabbit_exchange,
                queue=self.queue,
                routing_key=config.rabbit_routing_key
            )

            self.channel.basic_consume(
                queue=self.queue,
                on_message_callback=self.callback_factory(channel=self.channel),
                auto_ack=True,
            )

            logger.debug('[*] waiting for %s messages' % self.queue)

            self.channel.start_consuming()

    def callback_factory(self, channel: BlockingChannel) -> Callable:
        def callback(ch: BlockingChannel, method, properties, body: bytes) -> None:
            event_data = json.loads(body)
            logger.debug(f'Get data - {event_data}')

            event_type = event_data.get('event_type')
            template_id = TEMPLATE_ID.get(event_type)
            is_promo = False if template_id == 1 else True

            users = [event_data['payload']['users_id'], ]

            films = event_data['payload'].get('films')
            if films:
                context = {'films': films}
            else:
                template_id = 1
                context = {}

            notification = Event(
                id=uuid.uuid4(),
                is_promo=is_promo,
                template_id=template_id,
                user_ids=users,
                context=context
            )

            logger.debug(f'Prepared notification for send - {notification}')
            self.worker.do(notification)

        return callback
