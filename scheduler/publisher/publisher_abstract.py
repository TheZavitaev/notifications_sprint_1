from abc import abstractmethod, ABC
from typing import Any, Dict


class PublisherAbstract(ABC):
    @abstractmethod
    def publish(self, data: Dict[Any, Any]):
        pass
