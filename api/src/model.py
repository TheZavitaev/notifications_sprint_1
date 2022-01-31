from enum import Enum
from typing import Dict

from pydantic import BaseModel


class Transport(str, Enum):
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
    transport: Transport
    event_type: EventType
    payload: Dict
