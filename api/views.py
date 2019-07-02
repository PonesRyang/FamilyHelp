from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.filters import StarStaffFilterSet
from api.models import Users, Roles, Orders, OrderType, District
from api.serializers import StarStaffSerializer, OrdersTypeSerializer, DistrictSimpleSerializer, \
    DistrictDetailSerializer


class StarStaffView(ListAPIView):
    """查看星级家政人员"""
    queryset = Users.objects.all()
    serializer_class = StarStaffSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = StarStaffFilterSet

    def get_queryset(self):
        role = Roles.objects.filter(r_code=1)
        queryset = Users.objects.filter(role=role)
        return queryset


class OrdersTypeViewSet(ModelViewSet):
    queryset = OrderType.objects.all()
    serializer_class = OrdersTypeSerializer
    pagination_class = None


# 获取所有省级行政单位 - GET /api/districts/
class ProvinceView(ListAPIView):
    """查看各省的id和名称"""
    # only defer 优化SQL查询
    queryset = District.objects.filter(parent__isnull=True).only('distid',)
    # queryset = District.objects.filter(parent__isnull=True).defer('ishot','intro')
    serializer_class = DistrictSimpleSerializer
    pagination_class = None


# 获取指定行政单位详情及其管辖的行政单位 - GET /api/districts/{行政单位编号}
class DistrictView(RetrieveAPIView):
    """查看各省的id,名称,介绍及其下各市区的id和名称"""
    queryset = District.objects.all()
    serializer_class = DistrictDetailSerializer

