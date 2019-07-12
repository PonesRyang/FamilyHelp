from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views
from api.views import ArticleAPIView, OrderViewsSet, comments, complain, add_star_article, user_info, \
	order_finish_or_cancel, SubmitList, StarStaffView, ProvinceView, DistrictView, OrdersTypeViewSet, WalletAPIView


urlpatterns = [
	path('personal_information/', views.change_information),
	path('logout/', views.logout),
	path('article/', ArticleAPIView.as_view()),
	path('comment/', comments),
	path('complain/', complain),
	path('star_article/', add_star_article),
	path('mobile/<str:tel>/', views.send_mobile_code),
	path('login/', views.login),
	path('captcha/', views.get_captcha),
	path('user_info/', user_info),
	path('order_status/', order_finish_or_cancel),
	path('submitlist/', SubmitList, name='submitlist'),
	path('staff/', StarStaffView.as_view()),
	path('districts/', ProvinceView.as_view()),
	path('districts/<int:pk>', DistrictView.as_view()),
	path('wallet/', WalletAPIView.as_view()),
]

router = DefaultRouter()

router.register('order', OrderViewsSet)
router.register('order_type', OrdersTypeViewSet)


urlpatterns += router.urls
