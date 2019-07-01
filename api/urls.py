from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import OrderViewsSet, comments

urlpatterns = [
    path('comment/', comments),
]

router = DefaultRouter()

router.register('order', OrderViewsSet)

urlpatterns += router.urls
