from django.db import models
from django.contrib import auth
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User as AuthUser

# Create your models here.


# class MyUser(models.Model):
# User需要从auth里面继承，因为在用户认证里，程序只认auth里的User
class User(AuthUser):
    # id = models.AutoField(primary_key=True)
    # username = models.CharField(max_length=128, unique=True)
    # password = models.CharField(max_length=256)
    # email = models.EmailField(unique=True)
    # c_time = models.DateTimeField(auto_now_add=True)
    user_image_url = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username

    class Meta:
        # ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


# 当创建用户时，为每一个用户创建一个token
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
