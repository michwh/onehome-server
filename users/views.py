from django.shortcuts import render, redirect
from rest_framework import viewsets
from users.serializers import *
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from config_default import configs
from qiniu import Auth
import time
import random
import string
from rest_framework.authtoken.models import Token

import pdb

from django.contrib.auth.hashers import make_password, check_password


# 注册
class UserRegisterAPIView(APIView):
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        if User.objects.filter(username__exact=data.get('username')):
            return Response({"stateCode": 201, "msg": "用户已存在"}, 201)
        if User.objects.filter(email__exact=data.get('email')):
            return Response({"stateCode": 202, "msg": "邮箱已被注册"}, 201)
        new_user = {
            'actual_name': data.get('actual_name'),
            'student_id': data.get('student_id'),
            'username': data.get('username'),
            'email': data.get('email'),
            'password': make_password(data.get('password')),
            'student_card_image_url': data.get('student_card_image_url')
        }
        # print(new_user)
        serializer = RegisterSerializer(data=new_user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"stateCode": 200, "msg": "注册成功"}, 200)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# 登录
class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        try:
            user = User.objects.get(username__exact=username)
        except User.DoesNotExist:
            user = None
        if user:
            if check_password(password, user.password):
                serializer = UserSerializer(user)
                new_data = serializer.data
                # 记忆已登录用户，作为用户是否拥有某项权限的认证
                # self.request.session['user_username'] = user.username
                token = Token.objects.get(user_id=user.id)
                q = Auth(configs.get('qiniu').get('AK'), configs.get('qiniu').get('SK'))
                base_url = configs.get('qiniu').get('domain') + '/'
                user_image_url = q.private_download_url(base_url + new_data.get('user_image_url'), expires=86400)
                timeArray = time.strptime(str(user.last_login), "%Y-%m-%d %H:%M:%S")
                new_obj = {
                    'id': user.id,
                    # 'password': user.password,
                    'username': new_data.get('username'),
                    'token': token.key,
                    'user_image_url': user_image_url,
                    'last_login': time.mktime(timeArray),
                }
                # print(time.mktime(timeArray))
                user.last_login = time.strftime("%Y-%m-%d %H:%M:%S")
                user.save(update_fields=['last_login'])
                return Response({"stateCode": 200, "msg": new_obj}, status=HTTP_200_OK)
            else:
                return Response({"stateCode": 202, "msg": "密码不正确"}, 202)  # 密码不正确
        else:
            return Response({"stateCode": 201, "msg": "用户不存在"}, 201)  # 用户不存在


# 生成商品图片上传的token
class ImgUploadTokenAPIView(APIView):
    def post(self, request, format=None):
        data = request.data
        filetype = data.get('filetype')
        # if request.user.is_authenticated:
        # 构建鉴权对象
        q = Auth(configs.get('qiniu').get('AK'), configs.get('qiniu').get('SK'))

        # 生成图片名
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        key = salt + '_' + str(int(time.time())) + '.' + filetype

        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(configs.get('qiniu').get('bucket_name'), key, 3600)
        return Response({"stateCode": 200, "token": token, "key": key}, 200)
        # else:
        #     return Response({"stateCode": 201, "msg": "您没有权限执行此操作"}, 201)


# 上传用户头像
class ChangeAvatarAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            data = request.data
            user_image_url = data.get('user_image_url')
            q = Auth(configs.get('qiniu').get('AK'), configs.get('qiniu').get('SK'))
            username = str(request.user)
            try:
                user = User.objects.get(username__exact=username)
            except User.DoesNotExist:
                user = None
            user.user_image_url = user_image_url
            # 一定要加上这句话，要不然数据库数据不会更新
            user.save(update_fields=['user_image_url'])
            user_image_url = q.private_download_url(user_image_url, expires=86400)
            token = Token.objects.get(user_id=user.id)
            new_obj = {
                # 'username': username,
                # 'token': token.key,
                'user_image_url': user_image_url
            }
            return Response({"stateCode": 200, "msg": new_obj}, status=HTTP_200_OK)
        else:
            return Response({"stateCode": 201, "msg": "您没有权限执行此操作"}, 201)


# 修改密码
class ChangePasswordAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            data = request.data
            password = make_password(data.get('password'))
            username = str(request.user)
            try:
                user = User.objects.get(username__exact=username)
            except User.DoesNotExist:
                user = None
            user.password = password
            user.save(update_fields=['password'])
            return Response({"stateCode": 200, "msg": "操作成功"}, status=HTTP_200_OK)
        else:
            return Response({"stateCode": 201, "msg": "您没有权限执行此操作"}, 201)
