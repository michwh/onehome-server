from rest_framework import serializers
from collection.models import *


class Collection(serializers.ModelSerializer):
    class Meta:
        exclude = []
        model = Collection
        fields = "__all__"
