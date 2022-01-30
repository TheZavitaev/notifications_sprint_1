from enum import Enum
from typing import Dict, Any, List, Optional

from pydantic.main import BaseModel


class Priority(Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class Event(BaseModel):
    id: int
    is_promo: bool
    priority: Priority
    template_id: int
    user_ids: Optional[List[str]]
    context: Dict[str, Any]

    class Config:
        use_enum_values = True


class Template(BaseModel):
    title: str
    code: str
    template: str
    subject: str
