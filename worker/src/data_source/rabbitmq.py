import json
import logging
from typing import Any, Dict, Optional

import backoff
import pika
from pika import channel as pika_channel  # noqa: F401

# from .abstract import DataSourceAbstract
# from config import config
from abstract import DataSourceAbstract
from worker.src.config import config
from worker.src.models import Event

logger = logging.getLogger(__name__)


class DataSourceRabbitMQ(DataSourceAbstract):
    credentials = pika.PlainCredentials(
        config.rabbit_username,
        config.rabbit_password,
    )
    parameters = pika.ConnectionParameters(
        config.rabbit_host,
        credentials=credentials,
    )

    def __init__(self):
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

    def on_message(
            self,
            _unused_channel: pika_channel.Channel,
            basic_deliver: pika.spec.Basic.Deliver,
            _properties: pika.spec.BasicProperties,
            body: bytes,
    ):
        event_data = self.decode_data(body, basic_deliver.delivery_tag)
        if event_data is None:
            self.channel.basic_ack(basic_deliver.delivery_tag)

        is_promo = None
        template_id = None
        users = None
        context = None

        try:
            if event_data.get('payload'):
                template_id = event_data.get('event_type')
                transport = event_data["transport"]
                users = event_data['payload']['users_id']
                films = event_data['payload']['films']
                user_categories = event_data['payload']['user_categories']
                is_promo = True
                context = [films, user_categories]

            else:
                event_type = 'common'
                transport = 'email'
                users = event_data.get('user_id')
                is_promo = False
                context = []

        except KeyError as ex:
            logger.error(ex)

        notification = Event(is_promo=is_promo, template_id=template_id, user_ids=users, context=context)


        self.channel.basic_ack(basic_deliver.delivery_tag)



    def get_data(self) -> Optional[Dict[Any, Any]]:
        # get data from rabbit and return json
        #     {
        #       "id": 2,
        #       "is_promo": true,
        #       "template_id": 3,
        #       "user_ids": [
        #         "894cd492-a3bc-424c-895f-1f2772074304",
        #         "6c88ad4d-a9f7-440f-ba22-45d00c41a072",
        #         "8509b63e-aceb-431f-9008-665ffff772d0",
        #         "581defac-e938-44f5-971a-00db5c4031df",
        #         "80fd41eb-9a85-4995-a127-9c12c7a2493f"
        #       ],
        #       "context": {}
        #     },
        pass

