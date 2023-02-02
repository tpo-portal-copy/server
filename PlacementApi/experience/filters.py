import  django_filters
from .models import Experience


class ExperienceFilter(django_filters.FilterSet):
    class Meta:
        model = Experience
        fields = ('company__name','student__batch_year','roles','selected','jobtype','difficulty')


