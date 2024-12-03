import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')


MAX_LENGTH_ORIGINAL_LINK = 256
MAX_LENGTH_SHORT_LINK = 16
MAX_LENGTH_RANDOM_STRING = 6
ALL_SYMBOLS = string.ascii_letters + string.digits