import http
import logging

import backoff
import pika

from config import settings
from model import Event
from fastapi import FastAPI, HTTPException

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)


@app.on_event('startup')
def init_queue():
    global connection
    global channel

    credentials = pika.PlainCredentials(
        settings.rabbit_username,
        settings.rabbit_password,
    )
    parameters = pika.ConnectionParameters(
        settings.rabbit_host,
        credentials=credentials,
    )

    @backoff.on_exception(backoff.expo, pika.exceptions.AMQPConnectionError)
    def _connect():
        return pika.BlockingConnection(parameters=parameters)

    connection = _connect()
    channel = connection.channel()

    channel.exchange_declare(
        exchange=settings.rabbit_exchange,
        exchange_type=settings.rabbit_exchange_type,
        durable=True,
    )
    channel.queue_declare(queue=settings.rabbit_events_queue_name, durable=True)

    logger.info('Connected to queue.')


@app.on_event('shutdown')
def shutdown_event():
    logger.info('Closing queue connection.')
    connection.close()


@app.post('/api/v1/event', status_code=http.HTTPStatus.CREATED)
def put_event_to_queue(event: Event):
    try:
        channel.basic_publish(
            exchange=settings.rabbit_exchange,
            routing_key=settings.rabbit_events_queue_name,
            body=event.json(),
        )
    except Exception as err:
        logger.error(f'ERROR - queue publishing error: {str(err)}')
        raise HTTPException(
            http.HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='500: Internal server error. Please try later.',
        )

    return {'201': 'Created'}
