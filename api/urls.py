from django.urls import path, include
from rest_framework.routers import DefaultRouter


from api import views
from api.views import ArticleAPIView,OrderViewsSet, comments, complain,user_info, order_finish_or_cancel,StarStaffView, OrdersTypeViewSet, DistrictView, ProvinceView

urlpatterns = [
    path('personal_information/', views.change_information),
    path('logout/', views.logout),
    path('article/', ArticleAPIView.as_view()),
    path('comment/', comments),
    path('complain/', complain),
    path('user_info/', user_info),
    path('order_status/', order_finish_or_cancel),
    path('staff/', StarStaffView.as_view()),
    path('districts/', ProvinceView.as_view()),
    path('districts/', DistrictView.as_view()),
]

router = DefaultRouter()

router.register('order', OrderViewsSet)
router.register('order_type', OrdersTypeViewSet)


urlpatterns += router.urls

