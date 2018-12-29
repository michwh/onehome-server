from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from .models import Product, ProductImags
from .serializers import ProductSerializer, ProductImagesSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework import status
from .forms import UploadFileForm
from users.models import User
from rest_framework.renderers import JSONRenderer
from config_default import configs
from qiniu import Auth

# Create your views here.


# 获取商品列表
class ProductListViewset(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return Response(data, status=HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data, status=HTTP_200_OK)


# 获取商品图片列表
class ProductImagesListViewset(viewsets.ModelViewSet):

    queryset = ProductImags.objects.all()
    serializer_class = ProductImagesSerializer

    def get(self, request, format=None):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return Response(data, status=HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data, status=HTTP_200_OK)

