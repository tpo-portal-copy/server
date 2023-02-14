import django_filters
from .models import Student,StudentPlacement,StudentNotSitting,StudentIntern
from django.db.models import Q

class StudentFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='branch__branch_name',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='course__name',lookup_expr='iexact')
    class Meta:
        model = Student
        fields = ['student','cgpi','branch','course','pwd']
    


class StudentPlacementFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='student__cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='student__branch__branch_name',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='student__course__name',lookup_expr='iexact')
    cluster = django_filters.CharFilter(method='filter_by_cluster')
    pwd = django_filters.BooleanFilter(field_name='student__pwd')
    class Meta:
        model = StudentPlacement
        fields = ['student','cgpi','branch','course','cluster','pwd']
    def filter_by_cluster(self,queryset,name,value):
        return queryset.filter(Q(cluster__cluster_1 = value) | Q(cluster__cluster_3 = value) | Q(cluster__cluster_2 = value))


class StudentInternFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='student__cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='student__branch__branch_name',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='student__course__name',lookup_expr='iexact')
    pwd = django_filters.BooleanFilter(field_name='student__pwd')
    
    class Meta:
        model = StudentIntern
        fields = ['student','cgpi','branch','course','pwd']

class StudentNSFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='student__cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='student__branch__branch_name',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='student__course__name',lookup_expr='iexact')
    reason = django_filters.CharFilter(field_name='reason',lookup_expr='iexact')
    class Meta:
        model = StudentNotSitting
        fields = ['student','cgpi','branch','course','reason']
        