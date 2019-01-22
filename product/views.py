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
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import json
from django.core import serializers
# Create your views here.


# 对商品列表进行整理
def sort_out_list(request, data):
    # 构建鉴权对象
    q = Auth(configs.get('qiniu').get('AK'), configs.get('qiniu').get('SK'))
    new_data = []
    for obj in data:

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
        if product_user.user_image_url:
            product_avator_url = q.private_download_url(product_user.user_image_url, expires=3600)
        else:
            product_avator_url = None

        # 获取用户的收藏状态
        try:
            c = Collection.objects.get(username=str(request.user), product_id=obj.get('id'))
        except Collection.DoesNotExist:
            c = None
        if c:
            collect_state = True
        else:
            collect_state = False

        # 对时间字符串进行整理
        date = obj.get('c_time').split(".")[0]
        year = date.split("T")[0]
        time = date.split("T")[1]

        new_obj = {
            'product_id': obj.get('id'),
            'username': obj.get('username'),
            'avator_url': product_avator_url,
            'goods_price': obj.get('goods_price'),
            'goods_img_url': imgs,
            'collect_state': collect_state,
            'title': obj.get('title'),
            'description': obj.get('description'),
            'time': year + " " + time
        }
        new_data.append(new_obj)

    msg = {
        'stateCode': 200,
        'list': new_data
    }

    return msg


# 获取商品列表
class ProductListViewset(viewsets.ModelViewSet):

    def get(self, request):
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
            # print('ser.data的类型：' + str(ser.data))
            msg = sort_out_list(request, ser.data)
            return Response(msg, status=HTTP_200_OK)
        else:
            msg = {
                'stateCode': 201,
                'msg': '没有访问权限'
            }
            return Response(msg, 201)


# 获取搜索列表，暂时不分页
class SearchListViewset(viewsets.ModelViewSet):

    def get(self, request):
        if request.user.is_authenticated:

            # data = request.data
            key = request.GET.get('key')
            search_list = Product.objects.filter(title__contains=key)
            # paginator = Paginator(search_list, 5)
            # try:
            #     search = paginator.page(data.get('page'))
            # except PageNotAnInteger:
            #     search = paginator.page(1)
            # except EmptyPage:
            #     search = paginator.page(paginator.num_pages)
            # # print(search)
            # search_list = json.loads(serializers.serialize("json", search_list))
            ser = ProductSerializer(instance=search_list, many=True)
            # print(ser.data)
            msg = sort_out_list(request, ser.data)
            return Response(msg, 200)
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

        if request.user.is_authenticated:
            # print(data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"stateCode": 200, "msg": "发布成功"}, 200)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"stateCode": 201, "msg": "没有上传权限"}, 201)
