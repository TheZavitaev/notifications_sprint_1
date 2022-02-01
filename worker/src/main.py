import logging
import time

from config import config
from data_source.factory import DataSourceFactory
from db.postgres import Postgres
from email_sender.factory import EmailSenderFactory
from user_service_client.client import UserServiceClient
from worker import Worker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    postgres = Postgres()
    data_source = DataSourceFactory.get(config.DATA_SOURCE_TYPE)
    user_service_client = UserServiceClient()
    email_sender = EmailSenderFactory.get_sender(config.EMAIL_SENDER_TYPE)

    worker = Worker(
        postgres=postgres,
        data_source=data_source,
        user_service_client=user_service_client,
        email_sender=email_sender
    )

    while True:
        worker.do()
        time.sleep(config.WORKER_SLEEP_TIME)


if __name__ == '__main__':
    main()
