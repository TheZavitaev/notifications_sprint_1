from enum import Enum
from typing import Any, Dict, List

from pydantic.main import BaseModel


class Priority(Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class BaseContext(BaseModel):
    user_ids: List[str]
    user_categories: List[str]


class Event(BaseModel):
    id: int
    is_promo: bool
    priority: Priority
    context: Dict[Any, Any]

    class Config:
        use_enum_values = True
