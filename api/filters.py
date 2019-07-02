import django_filters

from api.models import Roles, Users
from django.db.models import Q


class StarStaffFilterSet(django_filters.FilterSet):

    u_relname_or_u_tel = django_filters.CharFilter(method='search', label='请输入查询家政人员的姓名或电话')

    @staticmethod
    def search(queryset, name, value):

        return queryset.filter(Q(u_relnam__icontains=value)) | Q(u_tel=value)


