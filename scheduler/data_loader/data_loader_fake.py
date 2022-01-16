import json

from models import Event, EventType
from .data_loader_abstract import DataLoaderAbstract


class DataLoaderFile(DataLoaderAbstract):

    def get_by_type(self, type: EventType) -> Event:
        with open('fixtures/data.json', 'r') as file:
            data = json.load(file)

        try:
            event_raw = data[type.value]
        except KeyError:
            raise Exception('Invalid event type')

        return Event.parse_obj(event_raw)
