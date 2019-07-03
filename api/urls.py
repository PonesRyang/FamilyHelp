from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

urlpatterns = [
    path('personal_information/', views.change_information),
    path('logout/', views.logout),
    path('mobile/<str:tel>/', views.send_mobile_code),
    # path('register/',views.register),
    path('login/',views.login),
    path('captcha/',views.get_captcha),

]

router = DefaultRouter()

# router.register('houseinfos', HouseInfoViewSet)

urlpatterns += router.urls
