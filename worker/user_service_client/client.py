from typing import Optional

import requests as requests

from config import config
from .client_abstract import UserServiceClientAbstract, UserInfo


class UserServiceClient(UserServiceClientAbstract):
    def get_user(self, user_id: str) -> Optional[UserInfo]:
        response = requests.get(config.USER_SERVICE_URL + 'user/' + user_id)
        if response.status_code == 404:
            return None
        response.raise_for_status()

        data = response.json()
        return UserInfo(**data)