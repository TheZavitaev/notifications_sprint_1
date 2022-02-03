import logging
from typing import Any, Dict, Optional

from jinja2 import Environment
from psycopg2 import sql

from context_collector.factory import ContextCollectorFactory, NotFoundException
from data_source.abstract import DataSourceAbstract
from db.postgres import Postgres
from email_sender.abstract import EmailSenderAbstract
from models import Event, Template
from user_service_client.client_abstract import UserInfo, UserServiceClientAbstract


class Worker:
    def __init__(self, postgres: Postgres,
                 user_service_client: UserServiceClientAbstract,
                 email_sender: EmailSenderAbstract):
        self.postgres = postgres
        self.user_service_client = user_service_client
        self.email_sender = email_sender

    def __get_template(self, template_id: int) -> Optional[Template]:
        query = sql.SQL("""
        select title, code, template, subject from notification_templates where id = %(id)s
                           """)

        items = self.postgres.exec(query, {'id': template_id})
        if len(items) != 1:
            logging.error(f'Error get template with id={template_id}')
            return None

        return Template(**items[0])

    def __gather_context(self, user_id: str, template_code: str) -> Dict[Any, Any]:
        context_collector_factory = ContextCollectorFactory(self.user_service_client)
        try:
            context_collector = context_collector_factory.create(template_code)
        except NotFoundException:
            # no context collector for this template type. Skip
            return {}
        return context_collector.collect(user_id)

    def __build_from_template(self, template: Template, user_info: UserInfo, context: Dict[Any, Any]) -> str:
        user_context = user_info.dict(include={'first_name', 'last_name'})
        context.update(user_context)

        env = Environment(autoescape=True)
        template_obj = env.from_string(template.template)
        return template_obj.render(**context)

    def do(self, event):
        logging.debug('Do work')

        # Получить шаблон
        template = self.__get_template(event.template_id)
        if not template:
            return
        for user_id in event.user_ids:
            # Получить информацию о пользователе
            user_info = self.user_service_client.get_user(user_id)
            if not user_info:
                logging.error(f'User {user_id} not found')
                continue
            # Проверить разрешил ли пользователь получать промо
            if event.is_promo and not user_info.promo_agree:
                logging.info('User is not agreed to receive promo messages. Skip')
                continue

            # в зависимости от tempate_type собираем контекст
            context = self.__gather_context(user_id, template.code)
            context.update(event.context)
            # Шаблонизировать
            item_to_send = self.__build_from_template(template, user_info, context)
            # отправить дальше
            self.email_sender.send(user_info.email, template.subject, item_to_send)
        logging.info(f'Handled {len(event.user_ids)} notifications')
