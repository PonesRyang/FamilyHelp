from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views
from api.views import ArticleAPIView, OrderViewsSet, comments, complain, add_star_article

urlpatterns = [
    path('personal_information/', views.change_information),
    path('logout/', views.logout),
    path('personal_information/', views.change_information),
    path('logout/', views.logout),
    path('article/', ArticleAPIView.as_view()),
    path('comment/', comments),
    path('complain/', complain),
    path('star_article/', add_star_article),
    path('mobile/<str:tel>/', views.send_mobile_code),
    path('login/',views.login),
    path('captcha/',views.get_captcha),
]

router = DefaultRouter()

router.register('order', OrderViewsSet)

urlpatterns += router.urls
