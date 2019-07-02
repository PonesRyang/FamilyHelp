from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import OrderViewsSet, comments, complain

urlpatterns = [
    path('comment/', comments),
    path('complain/', complain),
]

router = DefaultRouter()

router.register('order', OrderViewsSet)

urlpatterns += router.urls
