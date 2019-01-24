from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from collection.serializers import *
from product.views import sort_out_list
from product.serializers import *


# 改变收藏状态
class CollectStateViewset(viewsets.ModelViewSet):
    def post(self, request):
        if request.user.is_authenticated:
            data = request.data
            if data.get('collect_state') is True:
                new_data = {
                    'product_id': data.get('product_id'),
                    'username': str(request.user)
                }
                serializer = CollectionSerializer(data=new_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    obj = {
                        'stateCode': 200,
                        'msg': '操作成功'
                    }
                    return Response(obj, status=HTTP_200_OK)
                else:
                    obj = {
                        'stateCode': 202,
                        'msg': '数据格式错误'
                    }
                    return Response(obj, 202)
            else:
                c = Collection.objects.get(username=str(request.user), product_id=data.get('product_id'))
                c.delete()
                obj = {
                    'stateCode': 200,
                    'msg': '操作成功'
                }
                return Response(obj, status=HTTP_200_OK)
        else:
            obj = {
                'stateCode': 201,
                'msg': '没有操作权限'
            }
            return Response(obj, 201)


# 获取收藏列表
class CollectionListViewset(viewsets.ModelViewSet):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                product_list = Product.objects.filter(collection__username=str(request.user))
            except Collection.DoesNotExist:
                product_list = None
            ser = ProductSerializer(instance=product_list, many=True)
            msg = sort_out_list(request, ser.data)
            return Response(msg, status=HTTP_200_OK)
        else:
            obj = {
                'stateCode': 201,
                'msg': '没有操作权限'
            }
            return Response(obj, 201)

