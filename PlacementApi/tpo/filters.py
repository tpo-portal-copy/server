import django_filters
from .models import Resources 


class ResourcesFilter(django_filters.FilterSet):
    branch = django_filters.CharFilter(field_name='branch',lookup_expr='iexact')
    class Meta:
        model = Resources
        fields = ["content_type","branch"]

class CompanyWiseFilter(django_filters.FilterSet):
    branch = django_filters.CharFilter(field_name='branch',lookup_expr='iexact')
    course = django_filters.CharFilter(field_name='course',lookup_expr='iexact')
    cluster = django_filters.NumberFilter(field_name='clusterc')
    roll = django_filters.CharFilter(field_name='rollNumber',lookup_expr='iexact')

