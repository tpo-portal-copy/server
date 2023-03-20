import django_filters
from .models import Resources 


class ResourcesFilter(django_filters.FilterSet):
    branch = django_filters.CharFilter(field_name='branch',lookup_expr='iexact')
    class Meta:
        model = Resources
        fields = ["content_type","branch"]