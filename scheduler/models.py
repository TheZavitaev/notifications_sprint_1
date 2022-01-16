from enum import Enum
from typing import List

from pydantic import BaseModel


class EventType(Enum):
    MAILING_WEEKLY = 'mailing_weekly'
    MAILING_MONTHLY = 'mailing_monthly'

    @staticmethod
    def from_string(s):
        try:
            return EventType(s)
        except KeyError:
            raise ValueError()


class TransportType(Enum):
    EMAIL = 'email'
    SMS = 'sms'


class Priority(Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class Event(BaseModel):
    event_type: EventType
    transport_type: TransportType
    promo: bool
    priority: Priority
    user_ids: List[str]
    user_categories: List[str]

    class Config:
        use_enum_values = True
