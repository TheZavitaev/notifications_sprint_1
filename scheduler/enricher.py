from abc import ABC, abstractmethod

from models import Event
from user_service_client.client_abstract import UserServiceClientAbstract


class EnricherAbstract(ABC):
    @abstractmethod
    def enrich(self, event: Event) -> Event:
        pass


class Enricher(EnricherAbstract):
    def __init__(self, user_service_client: UserServiceClientAbstract):
        self.user_client = user_service_client

    def enrich(self, event: Event) -> Event:
        for category in event.user_categories:
            users = self.user_client.get_users_for_category(category)
            event.user_ids.extend(users)
        event.user_categories = []
        return event
