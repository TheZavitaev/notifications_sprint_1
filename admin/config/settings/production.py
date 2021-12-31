import os
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("PG_DBNAME"),
        'USER': os.getenv("PG_USER"),
        'PASSWORD': os.getenv("PG_PASSWD"),
        'HOST': os.getenv("PG_HOST", "127.0.0.1"),
        'PORT': os.getenv("PG_PORT", "5432"),
    }
}
