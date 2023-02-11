import  django_filters
from .models import Experience,Role

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass
class ExperienceFilter(django_filters.FilterSet):
    # company = django_filters.CharFilter(field_name='company__name',lookup_expr='iexact')
    company = CharInFilter(field_name='company__name',lookup_expr='in')
    roles = CharInFilter(field_name='roles__role',lookup_expr='in')
    year = django_filters.NumberFilter(field_name='datetime',lookup_expr='year__iexact')


    class Meta:
        model = Experience
        fields = ('company','year','roles','selected','jobtype','difficulty')
    


