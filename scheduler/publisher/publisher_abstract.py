from abc import abstractmethod, ABC
from typing import Any, List


class PublisherAbstract(ABC):
    @abstractmethod
    def publish(self, data: List[Any]):
        pass
