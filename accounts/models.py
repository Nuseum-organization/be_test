from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

class User(AbstractUser):
  username = models.CharField(_('username'), max_length=15, unique=True ,blank=True)
  # email = models.EmailField(_('email adrress'), unique=True)

  # USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  objects = UserManager()

  def __str__(self):
    return self.username