from django.conf.urls import url, include
from product.views import *


app_name = 'product'

urlpatterns = [
    url(r'getList', ProductListViewset.as_view({'get': 'get'})),
    # 获取图片上传的token
    # url(r'getProductUploadToken', PorductUploadTokenViewset.as_view({'post': 'post'})),
    url(r'publish', PublishViewset.as_view({'post': 'post'}))
]
