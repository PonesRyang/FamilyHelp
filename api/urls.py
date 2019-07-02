from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import StarStaffView, OrdersTypeViewSet, DistrictView, ProvinceView

urlpatterns = [
    path('staff/', StarStaffView.as_view()),
    path('districts/', ProvinceView.as_view()),
    path('districts/', DistrictView.as_view()),
]

router = DefaultRouter()
router.register('order_type', OrdersTypeViewSet)

urlpatterns += router.urls