from rest_framework.routers import DefaultRouter

urlpatterns = [
        ]

router = DefaultRouter()

# router.register('houseinfos', HouseInfoViewSet)

urlpatterns += router.urls
