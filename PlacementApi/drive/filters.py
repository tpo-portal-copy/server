import django_filters
from .models import Drive
# from course.models import Cluster

class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass

class DriveFilters(django_filters.FilterSet):
    company = django_filters.CharFilter(field_name='company__name',lookup_expr='iexact')
    cluster = NumberInFilter(method = "check_cluster")
    class Meta:
        model = Drive
        fields = ['company']
    def check_cluster(self,queryset,name,value):
        
        drive_list = []
       
        for i in range(queryset.count()):
            # print(value)
            # print(queryset[i].id)
            id_list = []
            for r in queryset[i].job_roles.all():
                # print("r-cluster: ",r.cluster)
                if r.cluster not in value:
                    # print(r.cluster)
                    # queryset[i].job_roles = queryset[i].job_roles.exclude(id = r.id)
                    # print(r.id)
                    # print(queryset[i].job_roles.exclude(id = r.id))
                    # queryset[i].job_roles = queryset[i].job_roles.exclude(id = r.id)
                    # print("x")
                    # print(queryset[i].job_roles.all())
                    id_list.append(r.id)
            # queryset[i] = queryset[i].job_roles.exclude(id__in = id_list)
            # print(queryset[i].job_roles.all())
            if len(id_list) == queryset[i].job_roles.count():
                drive_list.append(queryset[i].id)
            

        return queryset.exclude(id__in = drive_list)


    # def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
    #     print(queryset[0].job_roles.all()[0].cluster)
    #     super().__init__(data, queryset, request=request)





