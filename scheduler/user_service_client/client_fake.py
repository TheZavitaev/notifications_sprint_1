import json
import logging
from typing import List

from .client_abstract import UserServiceClientAbstract


class UserServiceClientFake(UserServiceClientAbstract):
    def get_users_for_category(self, category: str) -> List[str]:
        with open('fixtures/users.json', 'r') as file:
            data = json.load(file)

        try:
            return data[category]
        except KeyError:
            logging.error('Category not found')
            return []
