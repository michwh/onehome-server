from django.conf.urls import url, include
from product.views import *


app_name = 'product'

urlpatterns = [
    # 获取商品列表
    url(r'getList', ProductListViewset.as_view({'get': 'get'})),
    # 发布
    url(r'publish', PublishViewset.as_view({'post': 'post'})),
    # 获取搜索列表
    url(r'getSearchList', SearchListViewset.as_view({'get': 'get'})),
    # 获取我的发布列表
    url(r'getMyPublishList', MyPublishListViewset.as_view({'get': 'get'})),
]
