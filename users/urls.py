from django.conf.urls import url
from users.views import *
from rest_framework import routers

app_name = 'users'
urlpatterns = [
    url(r'^register', UserRegisterAPIView.as_view()),
    url(r'^login', UserLoginAPIView.as_view()),
    url(r'^getProductUploadToken', PorductUploadTokenAPIView.as_view()),
]
