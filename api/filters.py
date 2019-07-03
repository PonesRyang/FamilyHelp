import django_filters

from api.models import Orders


class OrderFilterSet(django_filters.FilterSet):
    user = django_filters.NumberFilter(method='filter_by_user')

    @staticmethod
    def filter_by_user(queryset, name, value):
        return queryset.filter(u=value)

    class Meta:
        model = Orders
        fields = ('user', )
