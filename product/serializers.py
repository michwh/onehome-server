from rest_framework import serializers
from product.models import *
from users.models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = Product
        fields = "__all__"


class Collection(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = Collection
        fields = "__all__"
