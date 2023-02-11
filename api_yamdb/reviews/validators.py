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
    checked = re.search(r'^^[\w.@+-]+\Z', value)
    if checked is None or checked.group() != value:
        forbidden_simbol = value[0] if (
            checked is None
        ) else value[checked.span()[1]]
        raise ValidationError(f'Нельзя использовать символ {forbidden_simbol} '
                              'в username. Имя пользователя может содержать '
                              'только буквы, цифры и символы @/./+/-/_')
    return value
