from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    """
    Нельзя добавлять произведения, которые еще не вышли (год выпуска не может
    быть больше текущего).
    """
    if value > datetime.now().year:
        raise ValidationError(
            f'Введенный год {value} больше текущего года {datetime.now().year}'
        )
