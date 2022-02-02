from enum import Enum
from typing import Dict

from pydantic import BaseModel


class Transport(str, Enum):
    email = 'email'
    sms = 'sms'
    push = 'push'


class EventType(str, Enum):
    common = 'common'
    monthly_personal_statistic = 'monthly_personal_statistic'


class Mailing(BaseModel):
    transport: Transport
    event_type: EventType
    payload: Dict


class WelcomeNotification(Mailing):
    transport = Transport.email
    event_type = EventType.common
    payload: Dict
