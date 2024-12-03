import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .random_id import get_unique_short_id


def create_object_in_data_base_for_api(data):
    """
    Функия отвечающая за создание и сохранение объекта ссылки в базе данных,
    и за отображение в формате json.
    Параметры функции:
    1) data - переданный json преобразованный в словарь,
    2) id - целоче число, id запроса,
    3) short - идентификатор короткой ссылки.
    """
    link = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    link.from_dict(data)
    db.session.add(link)
    db.session.commit()
    return jsonify(
        {
            'url': link.original,
            'short_link': request.url_root + link.short
        }
    ), 201


@app.route('/api/id/', methods=['POST'])
def create_short_id():
    """Функция обрабатывающая POST-запрос на создание новой короткой ссылки."""
    try:
        data = request.get_json()
    except Exception:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] == '':
        short = get_unique_short_id()
        data['custom_id'] = short
        return create_object_in_data_base_for_api(
            data=data
        )
    if len(data['custom_id']) > 16 or \
            re.match('^[a-zA-Z0-9]+$', data['custom_id']) is None:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    return create_object_in_data_base_for_api(data=data)


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """
    Функция обрабатывающая GET-запрос на получение
    оригинальной ссылки по указанному короткому идентификатору.
    Параметры функции:
    1) short_id - конвертер пути, принимает строковое значение.
    """
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': link.original}), 200
