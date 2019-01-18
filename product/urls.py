from django.conf.urls import url, include
from product.views import *


app_name = 'product'

urlpatterns = [
    url(r'getList', ProductListViewset.as_view({'get': 'get'})),
    url(r'publish', PublishViewset.as_view({'post': 'post'}))
]
