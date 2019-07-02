from django.urls import path, include
from rest_framework.routers import DefaultRouter


from api import views
from api.views import ArticleAPIView,OrderViewsSet, comments, complain

urlpatterns = [
    path('personal_information/', views.change_information),
    path('logout/', views.logout),
    path('article/', ArticleAPIView.as_view()),
    path('comment/', comments),
    path('complain/', complain),
]

router = DefaultRouter()

router.register('order', OrderViewsSet)

urlpatterns += router.urls
