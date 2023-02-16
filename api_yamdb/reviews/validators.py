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
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError((
            f'{value} Имя пользователя содержит недопустимые символы!'))


def validate_year(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            f'Указанный год {value} больше текущего'
        )
