from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

ROLE_USER = 'user'
ROLE_ADMIN = 'admin'
ROLE_MODERATOR = 'moderator'

ROLE_CHOICES = (
    (ROLE_USER, 'Аутентифицированный пользователь'),
    (ROLE_MODERATOR, 'Модератор'),
    (ROLE_ADMIN, 'Администратор'),
)


class User(AbstractUser):
    role = models.CharField(max_length=max([len(r[0]) for r in ROLE_CHOICES]),
                            choices=ROLE_CHOICES,
                            default=ROLE_USER)
    bio = models.TextField(default='', blank=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message=('Имя пользователя должно быть не длинее 150 символов.'
                         'Допустимы буквы, цифры и символы: @/./+/-/_.')
            )
        ]
    )
    first_name = models.CharField(max_length=150, blank=True, )
    last_name = models.CharField(max_length=150, blank=True, )
    email = models.CharField(max_length=254, blank=True, )

    confirmation_code = models.IntegerField(default=0)

    @property
    def is_admin(self):
        return self.is_staff or self.role == ROLE_ADMIN

    @property
    def is_moderator(self):
        return self.role == ROLE_MODERATOR

    @property
    def is_user(self):
        return self.role == ROLE_USER

    class Meta:
        ordering = ['-id']
