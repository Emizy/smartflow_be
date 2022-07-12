import os
import sys
from decouple import config
from config.settings.settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'NAME': config['DB_NAME'],
        'ENGINE': config['DB_ENGINE'],
        'USER': config['DB_USER'],
        'PORT': config['DB_PORT'],
        'PASSWORD': config['DB_PASSWORD']
    }
}
