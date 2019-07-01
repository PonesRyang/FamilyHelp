from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import user_info, order_finish_or_cancel

urlpatterns = [
    path('user_info/', user_info),
    path('order_status/', order_finish_or_cancel),
]