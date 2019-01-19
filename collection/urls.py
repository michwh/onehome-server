from django.conf.urls import url, include
from collection.views import *


app_name = 'collection'

urlpatterns = [
    url(r'changeCollectState', CollectStateViewset.as_view({'post': 'post'})),
]