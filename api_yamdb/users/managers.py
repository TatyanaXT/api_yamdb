from django.contrib.auth.base_user import BaseUserManager

EMAIL_IS_EMPTY_ERROR = 'Электронная почта обязательна!'
SUPERUSER_STAFF_ERROR = 'У Superuser is_staff должен быть True'
SUPERUSER_SUPERUSER_ERROR = 'У Superuser is_superuser должен быть True'


class CustomUserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(EMAIL_IS_EMPTY_ERROR)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(SUPERUSER_STAFF_ERROR)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(SUPERUSER_SUPERUSER_ERROR)

        return self.create_user(email, password, **extra_fields)
