from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from api.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Base model for application user
    """
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=256)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.name} ({self.email})'
