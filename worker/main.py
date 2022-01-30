import logging
import time

from config import config
from data_source.data_source import DataSourceFake
from db.postgres import Postgres
from sender.email_sender_fake import EmailSenderFake
from user_service_client.client import UserServiceClient
from worker import Worker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    postgres = Postgres()
    data_source = DataSourceFake()
    user_service_client = UserServiceClient()
    email_sender = EmailSenderFake()

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
