from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from .models import Product
from product.serializers import *
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from collection.models import Collection
from rest_framework.renderers import JSONRenderer
from config_default import configs
from qiniu import Auth
import time
import random
import string
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
import requests
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
# Create your views here.


# 自定义分页类2
# class MyLimitOffsetPagination(LimitOffsetPagination):
#     # 默认显示的个数
#     default_limit = 5
#     # 当前的位置
#     offset_query_param = "offset"
#     # 通过limit改变默认显示的个数
#     limit_query_param = "limit"
#     # 一页最多显示的个数
#     max_limit = 10


# 获取商品列表
class ProductListViewset(viewsets.ModelViewSet):

    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer

    # 获取交易信息列表
    # def get(self, request, format=None):
    #     print(request)
    #     # 获取所有数据
    #     roles = Product.objects.all()
    #     # 创建分页对象
    #     pg = PageNumberPagination()
    #     # 获取分页的数据
    #     page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
    #     # 对数据进行序列化
    #     ser = ProductSerializer(instance=page_roles, many=True)
    #     return Response(ser.data, status=HTTP_200_OK)

    def get(self, request):
        # username = request.data.get('username')
        # print(request.user)

        # 用户权限认证
        # user_username = request.session.get('user_username')
        # user = None
        # if user_username is None:
        # try:
        #     user = User.objects.get(username__exact=username)
        #     self.request.session['user_username'] = user.username
        #     # user_username = request.session.get('user_username')
        # except User.DoesNotExist:
        #     user = None
        # if user:
        if request.user.is_authenticated:
            # 获取所有数据
            roles = Product.objects.all()
            # 创建分页对象
            pg = PageNumberPagination()
            # pg = MyLimitOffsetPagination()
            # 获取分页的数据
            page_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
            # 对数据进行序列化
            ser = ProductSerializer(instance=page_roles, many=True)

            # 构建鉴权对象
            q = Auth(configs.get('qiniu').get('AK'), configs.get('qiniu').get('SK'))

            new_data = []
            for obj in ser.data:

                # 获取商品图片链接，整理成数组
                imgs = []
                private_url = q.private_download_url(obj.get('goods_img1'), expires=3600)
                imgs.append(private_url)
                if obj.get('goods_img2'):
                    private_url = q.private_download_url(obj.get('goods_img2'), expires=3600)
                    imgs.append(private_url)
                if obj.get('goods_img3'):
                    private_url = q.private_download_url(obj.get('goods_img3'), expires=3600)
                    imgs.append(private_url)
                if obj.get('goods_img4'):
                    private_url = q.private_download_url(obj.get('goods_img4'), expires=3600)
                    imgs.append(private_url)

                # 获取商品用户头像
                product_username = obj.get('username')
                try:
                    product_user = User.objects.get(username__exact=product_username)
                except User.DoesNotExist:
                    product_user = None
                product_avator_url = q.private_download_url(product_user.user_image_url, expires=3600)

                # 获取用户的收藏状态
                # print(Collection.objects.get(username__exact=user.username))

                # 对时间字符串进行整理
                date = obj.get('c_time').split(".")[0]
                year = date.split("T")[0]
                time = date.split("T")[1]

                new_obj = {
                    'username': obj.get('username'),
                    'avator_url': product_avator_url,
                    'goods_price': obj.get('goods_price'),
                    'goods_img_url': imgs,
                    'collect_state': False,
                    'title': obj.get('title'),
                    'description': obj.get('description'),
                    'time': year + " " + time
                }
                new_data.append(new_obj)

            msg = {
                'stateCode': 200,
                'list': new_data
            }

            return Response(msg, status=HTTP_200_OK)
        else:
            msg = {
                'stateCode': 201,
                'msg': '没有访问权限'
            }
            return Response(msg, 201)


# 发布交易信息
class PublishViewset(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        # username = data.get('username')
        serializer = ProductSerializer(data=data)

        # user_username = request.session.get('user_username')

        # try:
        #     user = User.objects.get(username__exact=username)
        # except User.DoesNotExist:
        #     user = None
        # if user:
        if request.user.is_authenticated:
            # print(data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"stateCode": 200, "msg": "发布成功"}, 200)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"stateCode": 201, "msg": "没有上传权限"}, 201)
