from django.conf.urls import url, include
from rest_framework import routers

from product.views import ProductListViewset, PublishViewSet, ProductImagesViewSet, ProductImagesListViewset

router = routers.DefaultRouter()
router.register(r'getList', ProductListViewset)  # 获取商品列表
router.register(r'getImagesList', ProductImagesListViewset)  # 获取商品图片列表
router.register(r'publish', PublishViewSet, base_name='Publish')  # 发布商品消息
router.register(r'publishImages', ProductImagesViewSet, base_name='PublishImages')  # 发布商品图片


app_name = 'product'
urlpatterns = [
    url(r'', include(router.urls)),
]