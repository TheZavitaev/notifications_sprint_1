import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class DataSourceAbstract(ABC):
    @abstractmethod
    def get_data(self) -> Optional[Dict[Any, Any]]:
        pass


class DataSourceFake(DataSourceAbstract):
    def __init__(self):
        with open('fixtures/data_source.json', 'r') as file:
            self.data = json.load(file)
        self.index = 0

    def get_data(self) -> Optional[Dict[Any, Any]]:
        try:
            item = self.data['items'][self.index]
        except IndexError:
            return None
        self.index += 1
        return item
