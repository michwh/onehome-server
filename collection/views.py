from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from collection.serializers import *


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
