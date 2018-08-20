from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from .models import Product, ProductImags
from .serializers import ProductSerializer, ProductImagesSerializer
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework import status
from .forms import UploadFileForm

# Create your views here.

# 获取商品列表
class ProductListViewset(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, format=None):
        serializer = ProductSerializer
        new_data = serializer.data
        return Response(new_data, status=HTTP_200_OK)

# 获取商品列表
class ProductImagesListViewset(viewsets.ModelViewSet):

    queryset = ProductImags.objects.all()
    serializer_class = ProductImagesSerializer

    def get(self, request, format=None):
        serializer = ProductImagesSerializer
        new_data = serializer.data
        return Response(new_data, status=HTTP_200_OK)

# 发布商品消息的另一种方法
class PublishViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImagesSerializer

# 商品图片
class ProductImagesViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImagesSerializer


