from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import MAX_LENGTH_SHORT_LINK


class YacutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=MAX_LENGTH_SHORT_LINK),
            Optional(),
            Regexp('^[a-zA-Z0-9]+$',
                   message='Указано недопустимое имя для короткой ссылки')
        ]
    )
    submit = SubmitField('Cоздать')
