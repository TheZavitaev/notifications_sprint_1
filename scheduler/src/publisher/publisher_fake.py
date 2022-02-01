import json
from pprint import pprint
from typing import Any, Dict

from .publisher_abstract import PublisherAbstract


class PublisherFake(PublisherAbstract):
    def publish(self, data: Dict[Any, Any]):
        print('-' * 60)
        pprint(data)

        with open('data.json', 'r') as file:
            file_data = json.load(file)

        file_data['items'].append(data)
        with open('data.json', 'w') as file:
            json.dump(file_data, file)

