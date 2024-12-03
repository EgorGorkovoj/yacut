import random

from settings import MAX_LENGTH_RANDOM_STRING, ALL_SYMBOLS
from .models import URLMap


def get_unique_short_id():
    """
    Функция отвечающая за автоматическое создание
    идентификатора короткой ссылки.
    """
    random_string = ''.join(
        random.choice(ALL_SYMBOLS) for _ in range(MAX_LENGTH_RANDOM_STRING)
    )
    if URLMap.query.filter_by(short=random_string).first() is not None:
        return get_unique_short_id()
    return random_string