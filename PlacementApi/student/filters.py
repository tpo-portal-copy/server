import django_filters
from .models import StudentPlacement

class StudentPlacementFilter(django_filters.FilterSet):
    class Meta:
        model = StudentPlacement
        fields = ['student__roll__username','student__cgpi','student__branch']
        