import random
import string

from flask import abort, flash, render_template, redirect

from . import app, db
from .models import URLMap
from .forms import YacutForm

ALL_SYMBOLS = string.ascii_letters + string.digits


def get_unique_short_id():
    """
    Функция отвечающая за автоматическое создание
    идентификатора короткой ссылки.
    """
    random_string = ''.join(random.choice(ALL_SYMBOLS) for _ in range(6))
    if URLMap.query.filter_by(short=random_string).first() is not None:
        return get_unique_short_id()
    return random_string


def create_object_in_data_base(form: YacutForm, short_link: str):
    """
    Функия отвечающая за создание и сохранение объекта ссылки в базе данных,
    и за отображение страницы пользователю с этими данными.
    Параметры функции:
    1) form - объект формы;
    2) short_link - идентификатор короткой ссылки.
    """
    link = URLMap(
        original=form.original_link.data,
        short=short_link
    )
    db.session.add(link)
    db.session.commit()
    flash('Ваша новая ссылка готова:\n')
    return render_template('add_yacut.html', form=form, link=link), 200


@app.route('/', methods=['GET', 'POST'])
def get_link():
    """View функция главной страницы сайта."""
    form = YacutForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if short == '' or short is None:
            short_link = get_unique_short_id()
            return create_object_in_data_base(form, short_link=short_link)
        if URLMap.query.filter_by(short=short).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('add_yacut.html', form=form), 200
        return create_object_in_data_base(form, short_link=short)
    return render_template('add_yacut.html', form=form), 200


@app.route('/<string:short>')
def redirect_by_short_link(short):
    """
    Функция отвечающая за переадресацию с короткой ссылки на исходную.
    Параметры функции:
    1) short - конвертер пути, принимает строковое значение.
    """
    link = URLMap.query.filter_by(short=short).first()
    if link is None or link == '':
        abort(404)
    return redirect(link.original)
