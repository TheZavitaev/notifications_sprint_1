from abc import ABC, abstractmethod

from models import EventType, Event


class DataLoaderAbstract(ABC):
    @abstractmethod
    def get_by_type(self, type: EventType) -> Event:
        pass
