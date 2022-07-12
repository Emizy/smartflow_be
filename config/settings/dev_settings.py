__author__ = 'EMiZY'

import os
import sys
from config.settings.settings import *

from decouple import config

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'NAME': config('DB_NAME'),
        'ENGINE': config('DB_ENGINE'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'OPTION': {
            'sql_mode': 'STRICT_ALL_TABLES'
        }
    }
}
