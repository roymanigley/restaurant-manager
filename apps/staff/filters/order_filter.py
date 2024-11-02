import django_filters

from apps.core.models import Order


class OrderFilter(django_filters.FilterSet):
    date_range = django_filters.DateRangeFilter(lookup_expr='end')

    class Meta:
        model = Order
        fields = '__all__'
