from rest_framework import serializers

from api.models import Users, District


class UsersSerializer(serializers.ModelSerializer):


    class Meta:
        model = Users
        fields = ('u_nickname',)


class DistrictSerializer(serializers.ModelSerializer):


    class Meta:
        model = District
        fields = ('name',)
