from django.conf.urls import url
from users.views import *
from rest_framework import routers

app_name = 'users'
urlpatterns = [
    url(r'^register', UserRegisterAPIView.as_view()),
    url(r'^login', UserLoginAPIView.as_view()),
    # 获取图片上传的token
    url(r'^getImgUploadToken', ImgUploadTokenAPIView.as_view()),
    # 上传头像
    url(r'changeAvatar', ChangeAvatarAPIView.as_view()),
    # 修改密码
    url(r'changePassword', ChangePasswordAPIView.as_view()),
]
