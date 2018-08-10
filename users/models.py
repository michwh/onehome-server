# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
#
# class User(AbstractUser):
#     nickname = models.CharField(max_length=50, blank=True)
#
#     class Meta(AbstractUser.Meta):
#         pass

from __future__ import unicode_literals
from django.db import models
from django.contrib import admin

# Create your models here


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)