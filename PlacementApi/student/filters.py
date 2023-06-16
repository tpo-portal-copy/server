import django_filters
from .models import Student,StudentPlacement,StudentNotSitting,StudentIntern,PPO, Placed, Offcampus
from course.models import Cluster
from django.db.models import Q, Exists, OuterRef
from django.utils import timezone
from rest_framework import exceptions
import datetime

# class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
#     pass
class PPOFilter(django_filters.FilterSet):
    # company = CharInFilter(field_name='company__name',lookup_expr='in')
    company = django_filters.CharFilter(field_name='company__name',lookup_expr='iexact')
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')

    class Meta:
        model = PPO
        fields = ['session','company','student']

class StudentFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='branch__branchName',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='course__name',lookup_expr='iexact')
    class Meta:
        model = Student
        fields = ['student','cgpi','branch','course','pwd']


class StudentTPOFilter(django_filters.FilterSet):
    chosenSession=""
    student = django_filters.CharFilter(field_name='roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='cgpi',lookup_expr='gte')
    branches = django_filters.CharFilter(field_name='branch__branchName',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='course__name',lookup_expr='iexact')
    eligibility = django_filters.CharFilter(method='filter_eligibility')
    session = django_filters.CharFilter(method='filter_session')

    # age = django_filters.RangeFilter(method='filter_age')
    minAge = django_filters.NumberFilter(method='filter_min_age')
    maxAge = django_filters.NumberFilter(method='filter_max_age')

    # intern related filters
    isBanned = django_filters.BooleanFilter(method='filter_isBanned')
    selected = django_filters.BooleanFilter(method='filter_isSelected')
    # isIntern = django_filters.BooleanFilter(method='filter_isIntern')

    # filter for gap year
    # filter for not sitting reason

    # placement related filters
    isNotSitting = django_filters.BooleanFilter(method='filter_isNotSitting')
    # isPlaced = django_filters.BooleanFilter(method='filter_isPlaced')
    placementType=django_filters.CharFilter(method='filter_placementType')
    isPlacedFirstCluster = django_filters.BooleanFilter(method='filter_isPlacedFirstCluster')

    isBasePlaced = django_filters.BooleanFilter(method='filter_isBasePlaced')
    # isMiddlePlaced = django_filters.BooleanFilter(method='filter_isMiddlePlaced')
    # isDreamPlaced denotes placement in a cluster greater than or equal to third cluster
    # isDreamPlaced = django_filters.BooleanFilter(method='filter_isDreamPlaced')

    class Meta:
        model = Student
        fields = ['student', 'cgpi', 'branch', 'course','pwd','gender', 'category','disability_type','disability_percentage']

    def filter_eligibility(self, queryset, name, value):
        if value=="placement" or value=="both":
            return queryset.filter(student_placement__isnull=False)
        elif value=="internship":
            return queryset.filter(Q(student_intern__isnull=False) & Q(student_placement__isnull=True))
        elif value=="other":
            return queryset.filter(Q(student_placement__isnull=True) & Q(student_intern__isnull=True))
        else:
            print("Eligibility cannot be ", value)
            return queryset.filter()

    def filter_session(self, queryset, name, value):
        self.chosenSession = value
        return queryset.filter()

    # def filter_age(self, queryset, name, value):
    #     from datetime import date
    #     # print(self.filters["session"])
    #     # print(self.form)
    #     print(self.filters['session'])
    #     # print(value.min)
    #     return queryset.filter()
    #     min_age, max_age, = value
    #     today = date.today()
    #     min_date_of_birth = date(today.year - max_age - 1, today.month, today.day)
    #     max_date_of_birth = date(today.year - min_age, today.month, today.day)
    #     return queryset.filter(date_of_birth__range=(min_date_of_birth, max_date_of_birth))
    #     pass

    def filter_min_age(self, queryset, name, value):
        if(value < 0):
            raise exceptions.NotAcceptable("Minimum age cannot be negative")
        today = datetime.date.today()
        min_date = today.replace(year=int(today.year-value))
        return queryset.filter(dob__lte=min_date)

    def filter_max_age(self, queryset, name, value):
        # print(name,value)
        if(value<0):
            raise exceptions.NotAcceptable("Maximum age cannot be negative")
        today = datetime.date.today()
        max_date = today.replace(year=int(today.year-value-1))
        return queryset.filter(dob__gt=max_date)
    # def filter_ageRange(self, queryset, name, value):
    #     age_start, age_stop = value.start, value.stop
    #     today = timezone.now()
    #     birth_date_start = today - timezone.timedelta(age_stop*365)
    #     birth_date_stop = today - timezone.timedelta(age_start*365+1)
    #     return queryset.filter(dob__lte=birth_date_start, dob__gte=birth_date_stop)

    def filter_isBanned(self, queryset, name, value):
        if value:
            return queryset.filter(banned_date__lte=timezone.now(), over_date__gte=timezone.now())
        else:
            return queryset.exclude(banned_date__lte=timezone.now(), over_date__gte=timezone.now())

    def filter_isSelected(self, queryset, name, value):
        if value:
            return queryset.filter(Q(student_intern__student_interned__isnull=False) | Q(student_placement__student_placed__isnull=False) | Q(student_ppo__isnull=False) | Q(student_offcampus__isnull=False))
        else:
            return queryset.filter(Q(student_intern__student_interned__isnull=True) & Q(student_placement__student_placed__isnull=True) & Q(student_ppo__isnull=True) & Q(student_offcampus__isnull=True))

    def filter_isNotSitting(self, queryset, name, value):
        value = not value
        return queryset.filter(student_ns__isnull=value)
        # if value:
        #     return queryset.filter(Exists(StudentNotSitting.objects.filter(student=OuterRef('pk'))))
        # else:
        #     return queryset.filter(~Exists(StudentNotSitting.objects.filter(student=OuterRef('pk'))))


    def filter_placementType(self, queryset, name, value):
        if value=="offcampus":
            return queryset.filter(student_offcampus__isnull=False)
        elif value=="oncampus":
            return queryset.filter(student_placement__student_placed__isnull=False)
        elif value=="ppo":
            return queryset.filter(student_ppo__isnull=False)
        else:
            raise exceptions.NotAcceptable("placement type cannot be anything other than offcampus, oncampus, ppo")

    # def filter_isPlaced(self, queryset, name, value):
    #     if value:
    #         return queryset.filter(Q(student_placement__student_placed__isnull=False) | Q(student_ppo__isnull=False) | Q(student_offcampus__isnull=False))
    #     else:
    #         return queryset.filter(Q(student_placement__student_placed__isnull=True) & Q(student_ppo__isnull=True) & Q(student_offcampus__isnull=True))

    def filter_isPlacedFirstCluster(self, queryset, name, value):
        print(self.chosenSession)
        if self.chosenSession=="":
            raise exceptions.APIException("You cannot see the placement statistics because there is no session given in query parameters")

        try:
            # getting the object of cluster 1
            cluster = Cluster.objects.get(session=self.chosenSession, starting=0)
        except Cluster.DoesNotExist:
            raise exceptions.APIException("Cluster 1 for current session does not exist")

        if value:
            return queryset.filter(Exists(Placed.objects.filter(job_role__ctc__range=(cluster.starting, cluster.ending))))
        else:
            return queryset.filter(~Exists(Placed.objects.filter(job_role__ctc__range=(cluster.starting, cluster.ending))))
            # return queryset.filter(~Exists(Placed.objects.filter(student=OuterRef('student_placement'))))

    def filter_isBasePlaced(self, queryset, name, value):
        return queryset.filter()
        pass


class StudentPlacementFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='student__cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='student__branch__branchName',lookup_expr='iexact')
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
    branch = django_filters.CharFilter(field_name='student__branch__branchName',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='student__course__name',lookup_expr='iexact')
    pwd = django_filters.BooleanFilter(field_name='student__pwd')
    
    class Meta:
        model = StudentIntern
        fields = ['student','cgpi','branch','course','pwd']

class StudentNSFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(field_name='student__roll__username',lookup_expr='iexact')
    cgpi = django_filters.NumberFilter(field_name='student__cgpi',lookup_expr='gte')
    branch = django_filters.CharFilter(field_name='student__branch__branchName',lookup_expr='iexact')
    course =django_filters.CharFilter(field_name='student__course__name',lookup_expr='iexact')
    reason = django_filters.CharFilter(field_name='reason',lookup_expr='iexact')
    class Meta:
        model = StudentNotSitting
        fields = ['student','cgpi','branch','course','reason']