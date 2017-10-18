from .models import Service
import django_filters

class ServiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Service
        fields = ['name', 'description', 'owner']
        order_by = ['pk']
		