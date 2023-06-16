import django_filters
from .models import Drive,JobRoles
from django.db.models import Prefetch,F,OuterRef,Subquery
from course.models import Cluster
# from course.models import Cluster

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

# from django.db.models import Q
class DriveFilters(django_filters.FilterSet):
    company = django_filters.CharFilter(field_name='company__name',lookup_expr='iexact')
    # cluster = NumberInFilter(method = "check_cluster",label='cluster')
    class Meta:
        model = Drive
        fields = ['company' ]
    # def check_cluster(self,queryset,name,value):  
    #     jobroles_prefetch = Prefetch('job_roles',queryset=JobRoles.objects.filter(cluster__in = value))
    #     queryset = queryset.prefetch_related(jobroles_prefetch)
    #     # return queryset

    #     drive_list = []
    #     for i in range(queryset.count()):
    #         if queryset[i].job_roles.count() == 0:
    #             drive_list.append(queryset[i].id)

    #     return queryset.exclude(id__in = drive_list)





