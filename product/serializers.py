from rest_framework import serializers
from product.models import *
from users.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = Product
        fields = "__all__"

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = ProductImags
        fields = "__all__"