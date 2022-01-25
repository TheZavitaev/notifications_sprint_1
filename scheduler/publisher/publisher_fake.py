from pprint import pprint
from typing import Any, Dict

from .publisher_abstract import PublisherAbstract


class PublisherFake(PublisherAbstract):
    def publish(self, data: Dict[Any, Any]):
        print('-' * 60)
        pprint(data)
