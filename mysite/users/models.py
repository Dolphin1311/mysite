from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        values = [email]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        # check if all fields are set
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError(f"The {field_name} must be set.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="E-mail")
    last_login = models.DateTimeField(null=True, verbose_name="Last login time")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Date joined")
    is_staff = models.BooleanField(default=False, verbose_name="Is stuff")
    is_active = models.BooleanField(default=True, verbose_name="Is activated account")

    objects = UserManager()

    USERNAME_FIELD = "email"
