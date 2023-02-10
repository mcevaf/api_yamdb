import re  # бибилотека регулярных выражений

from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Имя не может быть - me'),
            params={'value': value},
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Cимволы не могут быть в username - {value}', value),
            params={'valuse': value},
        )
