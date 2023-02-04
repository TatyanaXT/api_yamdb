from dataclasses import dataclass

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models

from .managers import CustomUserManager


@dataclass
class UserRole:
    """Класс для хранения ролей пользователей."""
    ADMIN: str = 'admin'
    DEFAULT_USER: str = 'user'
    MODERATOR: str = 'moderator'


ROLES = (
    (UserRole.ADMIN, 'администратор'),
    (UserRole.DEFAULT_USER, 'пользователь'),
    (UserRole.MODERATOR, 'медератор'),
)

UNIQUE_EMAIL_ERORR = 'Пользователь с таким email уже существует!'
UNIQUE_USERNAME_ERORR = 'Пользователь с таким username уже существует!'

ROLE_FIELD_MAX_LENGTH = 9
EMAIL_FIELD_MAX_LENGTH = 254
USERNAME_FIELD_MAX_LENGTH = 150


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""

    REQUIRED_FIELD = ('username', 'email')

    objects = CustomUserManager()

    bio = models.TextField(
        'Биография',
        blank=True
    )

    role = models.CharField(
        'Роль',
        choices=ROLES,
        default=UserRole.DEFAULT_USER,
        max_length=ROLE_FIELD_MAX_LENGTH,
    )

    email = models.EmailField(
        'Электронная почта',
        blank=False,
        unique=True,
        max_length=EMAIL_FIELD_MAX_LENGTH,
        error_messages={
            'unique': UNIQUE_EMAIL_ERORR,
        },
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_FIELD_MAX_LENGTH,
        unique=True,
        validators=[ASCIIUsernameValidator],
        error_messages={
            'unique': UNIQUE_USERNAME_ERORR,
        },
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    @property
    def is_admin(self):
        return (self.role == UserRole.ADMIN
                or self.is_staff
                or self.is_superuser)

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-date_joined']
