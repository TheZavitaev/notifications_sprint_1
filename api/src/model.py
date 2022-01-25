from datetime import datetime
from enum import Enum
from typing import Dict

from pydantic import BaseModel


class Service(str, Enum):  # надо ли?
    ugc = 'ugc'
    auth = 'auth'
    admin = 'admin'


class Source(str, Enum):  # и это? тут, наверное, надо очередь замутить
    email = 'email'
    sms = 'sms'
    push = 'push'


class EventType(str, Enum):
    welcome_letter = 'welcome_letter'
    selection_movies = 'selection_movies'
    personal_newsletter = 'personal_newsletter'

    mailing_weekly = 'mailing_weekly'
    mailing_monthly = 'mailing_monthly'

    security_notification = 'security_notification'


class Event(BaseModel):
    service: Service
    source: Source
    event_type: EventType
    scheduled_datetime: datetime
    payload: Dict
