from rest_framework import serializers
from users.models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = User
        fields = "__all__"
