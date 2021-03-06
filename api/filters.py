import django_filters
from api.models import Roles, Users,Orders
from django.db.models import Q


class StarStaffFilterSet(django_filters.FilterSet):

    u_relname_or_u_tel = django_filters.CharFilter(method='search', label='请输入查询家政人员的姓名或电话')

    @staticmethod
    def search(queryset, name, value):

        return queryset.filter(Q(u_relnam__icontains=value)) | Q(u_tel=value)

    @property  # 将ps方法编成一个属性
    def qs(self):
        parent = super(StarStaffFilterSet, self).qs
        q = Q()
        u_realname = self.request.query_params.get('u_realname')
        if u_realname:
            q |= Q(u_relname=u_realname)
        u_tel = self.request.query_params.get('u_tel')
        if u_tel:
            q |= Q(u_tel=u_tel)
        return parent.filter(q)


class OrderFilterSet(django_filters.FilterSet):
    user = django_filters.NumberFilter(method='filter_by_user')

    @staticmethod
    def filter_by_user(queryset, name, value):
        return queryset.filter(u=value)

    class Meta:
        model = Orders
        fields = ('user', )
