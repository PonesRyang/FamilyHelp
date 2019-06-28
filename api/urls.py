from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

urlpatterns = [
    path('personal_information/', views.change_information),
    path('logout/', views.logout)
]

router = DefaultRouter()

# router.register('houseinfos', HouseInfoViewSet)

urlpatterns += router.urls
