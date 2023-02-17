import datetime
import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """
    Недопустимо использовать имя пользователя me.
    """
    if value == 'me':
        raise ValidationError(
            ('Имя не может быть - me'),
        )
    value_check = set(re.sub(r'^[\w.@+-]+\Z', r'', value.join(set(value))))
    if value_check:
        raise ValidationError(
            f'Имя пользователя содержит недопустимые символы:{value_check}')


def validate_year(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            f'Указанный год {value} больше текущего'
        )
