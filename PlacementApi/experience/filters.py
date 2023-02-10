import  django_filters
from .models import Experience


class ExperienceFilter(django_filters.FilterSet):
    company = django_filters.CharFilter(field_name='company__name',lookup_expr='iexact')
    year = django_filters.NumberFilter(field_name='datetime',lookup_expr='year__iexact')


    class Meta:
        model = Experience
        fields = ('company','year','roles','selected','jobtype','difficulty')


