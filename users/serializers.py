from rest_framework import serializers
from users.models import *


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'c_time', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = User
        field = ('id', 'username')
