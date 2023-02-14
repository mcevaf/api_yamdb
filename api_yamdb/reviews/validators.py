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
            f'{value} Имя пользователя содержит не допустимые символы!'))
