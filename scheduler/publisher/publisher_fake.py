from pprint import pprint
from typing import Any, List

from .publisher_abstract import PublisherAbstract


class PublisherFake(PublisherAbstract):
    def publish(self, data: List[Any]):
        for i, item in enumerate(data, start=1):
            print(f'Chunk {i}')
            pprint(item)
