import os
import sys

from config.settings.settings import *
from decouple import config
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'NAME': config('DB_NAME'),
        'ENGINE': config('DB_ENGINE'),
        'USER': config('DB_USER'),
        'PORT': config('DB_PORT'),
        'PASSWORD': config('DB_PASSWORD')
    }
}

# herokuapp config
prod_db = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(prod_db)
