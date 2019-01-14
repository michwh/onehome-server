from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from .models import Product
from product.serializers import *
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework import status
from .forms import UploadFileForm
from users.models import User
from rest_framework.renderers import JSONRenderer
from config_default import configs
from qiniu import Auth
import time
import random
import string
from rest_framework.permissions import AllowAny

# Create your views here.


# 获取商品列表
class ProductListViewset(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # 获取交易信息列表
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


# 生成商品图片上传的token
# class PorductUploadTokenViewset(viewsets.ModelViewSet):
#     def post(self, request, format=None):
#         data = request.data
#         username = data.get('username')
#         filetype = data.get('filetype')
#         timestamp = data.get('timestamp')
#         # try:
#         #     user = User.objects.get(username__exact=username)
#         # except User.DoesNotExist:
#         #     user = None
#         user_username = request.session.get('user_username')
#         if username == user_username:
#             # 构建鉴权对象
#             q = Auth(configs.get('qiniu').get('AK'), configs.get('qiniu').get('SK'))
#
#             # 生成图片名
#             salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
#             key = salt + '_' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '.' + filetype
#
#             # 生成上传 Token，可以指定过期时间等
#             token = q.upload_token(configs.get('qiniu').get('bucket_name'), key, 3600)
#             return Response({"stateCode": 200, "token": token, "key": key, "timestamp": timestamp}, 200)
#         else:
#             return Response({"stateCode": 201, "msg": "没有上传权限"}, 201)


# 发布交易信息
class PublishViewset(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        username = data.get('username')
        serializer = ProductSerializer(data=data)

        # user_username = request.session.get('user_username')

        try:
            user = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            user = None
        if user:
            print(data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"stateCode": 200, "msg": "发布成功"}, 200)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"stateCode": 201, "msg": "没有上传权限"}, 201)
