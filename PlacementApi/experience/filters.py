import  django_filters
from .models import Experience
from drive.models import Role

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass
class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass
class ExperienceFilter(django_filters.FilterSet):
    # company = django_filters.CharFilter(field_name='company__name',lookup_expr='iexact')
    company = CharInFilter(field_name='company__name',lookup_expr='in')
    roles = CharInFilter(field_name='roles__name',lookup_expr='in')
    year = NumberInFilter(field_name='updated_at',lookup_expr='year__in')
    difficulty = CharInFilter(field_name='difficulty',lookup_expr='in')


    class Meta:
        model = Experience
        fields = ('company','year','roles','selected','jobtype','difficulty')
    


