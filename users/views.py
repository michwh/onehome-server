from django.shortcuts import render, redirect
from rest_framework import viewsets
from users.serializers import *
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


import pdb

# 注册
class UserRegisterAPIView(APIView):
   queryset = User.objects.all()
   serializer_class = UserRegisterSerializer
   permission_classes = (AllowAny,)

   def post(self, request, format=None):
       data = request.data
       username = data.get('username')
       if User.objects.filter(username__exact=username):
           return Response("用户名已存在",HTTP_400_BAD_REQUEST)
       serializer = UserRegisterSerializer(data=data)
       if serializer.is_valid(raise_exception=True):
           serializer.save()
           return Response(serializer.data,status=HTTP_200_OK)
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
        user = User.objects.get(username__exact=username)
        if user.password == password:
            serializer = UserSerializer(user)
            new_data = serializer.data
            # 记忆已登录用户，作为用户是否拥有某项权限的认证
            self.request.session['user_id'] = user.id
            return Response(new_data, status=HTTP_200_OK)
        return Response('password error', HTTP_400_BAD_REQUEST)
