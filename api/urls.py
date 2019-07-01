from django.urls import path

from api.views import DistrictViewSet, SubmitList

urlpatterns = [
    path('submitlist/',SubmitList, name='submitlist')
]