from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    invite = models.CharField(max_length=32, default=uuid4().hex, verbose_name='invite code')
    invitedby = models.IntegerField(default=0, verbose_name='invited by user\'s id')
