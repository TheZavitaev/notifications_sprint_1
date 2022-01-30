from typing import List

import requests as requests

from config import config
from .client_abstract import UserServiceClientAbstract


class UserServiceClient(UserServiceClientAbstract):
    def get_users_for_category(self, category: str) -> List[str]:
        response = requests.get(config.USER_SERVICE_URL + 'category/' + category)
        response.raise_for_status()

        data = response.json()
        return [user['id'] for user in data['users']]
