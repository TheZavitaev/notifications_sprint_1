import argparse
import copy
from typing import List

from config import config
from data_loader.data_loader_abstract import DataLoaderAbstract
from data_loader.data_loader_fake import DataLoaderFile
from enricher import EnricherAbstract, Enricher
from models import EventType, Event
from publisher.publisher_abstract import PublisherAbstract
from publisher.publisher_fake import PublisherFake
from user_service_client.client_fake import UserServiceClientFake


class Worker:
    def __init__(self, loader: DataLoaderAbstract, enricher: EnricherAbstract, publisher: PublisherAbstract):
        self.loader = loader
        self.enricher = enricher
        self.publisher = publisher

    def _bulker(event: Event) -> List[Event]:
        def create_chunks(list_name, step):
            for i in range(0, len(list_name), step):
                yield list_name[i: i + step]

        result = []

        for users_chunk in create_chunks(event.user_ids, config.PUBLISHER_CHUNK_SIZE):
            new_event = copy.deepcopy(event)
            new_event.user_ids = users_chunk
            result.append(new_event)
        return result

    def work(self, event_type: EventType):
        event = self.loader.get_by_type(event_type)
        event = self.enricher.enrich(event)

        events = Worker._bulker(event)
        events = [event.dict() for event in events]

        self.publisher.publish(events)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event_type", type=str, choices=[e.value for e in EventType], required=True)
    args = parser.parse_args()

    event_type = EventType.from_string(args.event_type)
    user_service_client = UserServiceClientFake()
    enricher = Enricher(user_service_client)

    worker = Worker(DataLoaderFile(), enricher, PublisherFake())
    worker.work(event_type)


if __name__ == '__main__':
    # event = Event(
    #     event_type=EventType.MAILING_WEEKLY,
    #     transport_type=TransportType.EMAIL,
    #     promo=True,
    #     priority=Priority.LOW,
    #     user_categories=['active']
    #
    # )
    #
    # with open('data.json', 'w') as file:
    #     file.write(event.json(indent=2))
    main()
