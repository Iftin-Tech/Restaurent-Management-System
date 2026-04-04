from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Overwrite databases block here if you need to use `.env` using python-decouple
# e.g.:
# from decouple import config 
# DATABASES['default']['PASSWORD'] = config('DB_PASSWORD')
