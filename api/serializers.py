from rest_framework import serializers

from api.models import Orders, Users


class OrderDetailSerializer(serializers.ModelSerializer):
    u_relname = serializers.SerializerMethodField()

    @staticmethod
    def get_u_relname(order):
        users = order.users_set.all()
        for user in users:
            if user.role.first().r_code != '0':
                return user.u_relname


    class Meta:
        model = Orders
        fields = ('order_money', 'u_relname', 'order_createtime', 'order_finishtime',
                  'order_number', 'order_addr', 'order_tips')