from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class DataSourceAbstract(ABC):
    @abstractmethod
    def get_data(self) -> Optional[Dict[Any, Any]]:
        pass
