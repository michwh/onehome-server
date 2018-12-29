from django.conf.urls import url, include
from product.views import *


app_name = 'product'

urlpatterns = [
    url(r'getList', ProductListViewset.as_view({'get': 'get'})),
    url(r'getImagesList', ProductImagesListViewset.as_view({'get': 'get'})),
]
