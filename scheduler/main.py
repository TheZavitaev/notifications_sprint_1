import copy
import logging
import time
from typing import List

from psycopg2 import sql

from config import config
from db.postgres import Postgres
from models import Event, BaseContext
from publisher.publisher_abstract import PublisherAbstract
from publisher.publisher_fake import PublisherFake
from user_service_client.client_abstract import UserServiceClientAbstract
from user_service_client.client_fake import UserServiceClientFake

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, postgres: Postgres, user_service: UserServiceClientAbstract, publisher: PublisherAbstract):
        self.postgres = postgres
        self.user_service = user_service
        self.publisher = publisher

    @staticmethod
    def __chunker(event: Event) -> List[Event]:
        """Разбивает событие на несколько чанков с ограниченным количеством user_ids в каждом чанке"""

        def create_chunks(list_name, step):
            for i in range(0, len(list_name), step):
                yield list_name[i: i + step]

        result = []

        for users_chunk in create_chunks(event.context['user_ids'], config.PUBLISHER_CHUNK_SIZE):
            new_event = copy.deepcopy(event)
            new_event.context['user_ids'] = users_chunk
            result.append(new_event)
        return result

    def get_user_ids(self, user_categories: List[str]):
        """Получить список пользователей, относящихся к переданому списку категорий"""
        ids = []
        for category in user_categories:
            ids.extend(self.user_service.get_users_for_category(category))
        return ids

    def mark_event_as_done(self, item_id: int):
        """Пометить запись как завершенную"""
        query = sql.SQL("""update mailing_tasks
                           set status = 'done',
                           execution_datetime = current_timestamp
                           where id = %(item_id)s;""")

        self.postgres.exec(query, {'item_id': item_id})

    def get_ready_events(self) -> List[Event]:
        """Получить все записи, готовые к обработке"""
        query = sql.SQL("""select id, is_promo, priority, context, scheduled_datetime, template_id from mailing_tasks
                           where scheduled_datetime < current_date
                           and status = 'pending'
                           order by scheduled_datetime
                           limit %(batch_size)s;""")

        items = self.postgres.exec(query, {'batch_size': config.SELECT_BATCH_SIZE})
        return [Event(**item) for item in items]

    def work(self):
        """Выбрать готовые записи и обработать их"""
        events = self.get_ready_events()
        logger.info(f'Handle {len(events)} events')
        for event in events:
            base_context = BaseContext(**event.context)

            user_ids = self.get_user_ids(base_context.user_categories)
            event.context['user_ids'].extend(user_ids)
            del event.context['user_categories']

            event_chunks = self.__chunker(event)

            for chunk in event_chunks:
                self.publisher.publish(chunk.dict())

            self.mark_event_as_done(event.id)


def main():
    scheduler = Scheduler(
        Postgres(),
        UserServiceClientFake(),
        PublisherFake()
    )

    while True:
        logger.info('Do work')
        scheduler.work()
        time.sleep(config.SCHEDULER_SLEEP_TIME)


if __name__ == '__main__':
    main()
