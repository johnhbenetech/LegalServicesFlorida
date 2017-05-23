from .models import Provider
import django_filters

class ProviderFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Provider
        fields = ['name', 'description', 'price', 'owner']
        order_by = ['pk']
		