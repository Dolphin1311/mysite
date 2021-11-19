from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from django.conf import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        values = [email, username]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))

        # check if all fields are set
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError(f'The {field_name} must be set.')

            email = self.normalize_email(email)
            user = self.model(email=email, username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type_id', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)


class UserType(models.Model):
    name = models.CharField(max_length=255)


# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='E-mail')
    username = models.CharField(unique=True, max_length=255, verbose_name='Username')
    last_login = models.DateTimeField(null=True, verbose_name='Last login time')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date joined')
    is_active = models.BooleanField(default=True, verbose_name='Online')
    is_staff = models.BooleanField(default=False, verbose_name='Is stuff')
    is_activated = models.BooleanField(default=False, verbose_name='Is activated account')
    user_type = models.ForeignKey(UserType, on_delete=models.PROTECT, verbose_name='User type')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Person(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    phone = PhoneNumberField(unique=True, verbose_name='Phone')
    date_birthday = models.DateField(verbose_name='Date of birth')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, primary_key=True)