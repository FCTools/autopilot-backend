"""
Copyright © 2020 FC Tools. All rights reserved.
Author: German Yakimov
"""

from .base import *

DEBUG = False

DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "176.57.68.50",
    "vm1409421.4ssd.had.wf",
    "localhost",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DATABASE_NAME,
        "USER": DATABASE_USER,
        "PASSWORD": DATABASE_PASSWORD,
        "HOST": DATABASE_HOST,
        "PORT": DATABASE_PORT,
    }
}
