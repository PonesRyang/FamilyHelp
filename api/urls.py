from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views
from api.views import ArticleAPIView

urlpatterns = [
	path('personal_information/', views.change_information),
	path('logout/', views.logout),
	path('article/', ArticleAPIView.as_view())
]

router = DefaultRouter()

# router.register('houseinfos', HouseInfoViewSet)

urlpatterns += router.urls
