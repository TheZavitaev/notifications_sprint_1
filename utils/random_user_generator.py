"""Утилита для генерации json с рандомными юзерами"""

import json
import random
import uuid

import requests as requests
from pydantic.main import BaseModel


class UserInfo(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    promo_agree: bool
    category: str


def generate_user() -> UserInfo:
    response = requests.get('https://randomuser.me/api/?nat=us')
    data = response.json()

    return UserInfo(
        id=str(uuid.uuid4()),
        first_name=data['results'][0]['name']['first'],
        last_name=data['results'][0]['name']['last'],
        email=data['results'][0]['email'],
        promo_agree=bool(random.getrandbits(1)),
        category='active' if random.randrange(10) < 9 else 'inactive'
    )


active = []
inactive = []
users = []
for i in range(0, 20):
    user = generate_user()
    users.append(user.dict())
    print(user)
    if user.category == 'active':
        active.append(user.id)
    else:
        inactive.append(user.id)

with open('users.json', 'w') as file:
    json.dump({'users': users}, file)

categories = {
    "active": active,
    "inactive": inactive
}
with open('user_categories.json', 'w') as file:
    json.dump(categories, file)
