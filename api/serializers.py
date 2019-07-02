from rest_framework import serializers

from api.models import Users, Roles, OrderType, District


class RolesSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Roles
        fields = '__all__'


class StarStaffSerializer(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()

    @staticmethod
    def get_roles(user):

        return RolesSimpleSerializer(user.role.r_name, many=True).data

    class Meta:
        model = Users
        fields = ('u_relname', 'u_tel', 'u_birthday', 'u_photo', 'star_lv', 'u_intro')


class OrdersTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderType
        fields = ('order_type_name',)


class DistrictSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = ('distid', 'name')


class DistrictDetailSerializer(serializers.ModelSerializer):

    cities = serializers.SerializerMethodField()

    @staticmethod
    def get_cities(district):
        queryset = District.objects.filter(parent=district)
        return DistrictSimpleSerializer(queryset, many=True).data

    class Meta:
        model = District
        fields = ('distid', 'name', 'cities')







