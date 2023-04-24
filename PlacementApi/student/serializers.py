from rest_framework import serializers
from rest_framework.exceptions import APIException
from .models import Student,StudentIntern,StudentNotSitting,StudentPlacement,PPO,Offcampus,Placed,Interned,City,Cluster,ClusterChosen,State
from django.contrib.auth.models import User
from course.models import Course,Specialization,CourseYearAllowed
from company.models import Company
from django.db.models import Q
from django.utils import timezone


class PPOSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    student = serializers.CharField(source = 'student.roll.username')

    class Meta:
        model = PPO
        fields = '__all__'

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']


class ClusterSerializer(serializers.ModelSerializer):
    range = serializers.SerializerMethodField()
    class Meta:
        model = Cluster
        exclude = ['starting','ending']
    
    def get_range(self,item):
        return "{0}-{1} LPA".format(item.starting,item.ending)

class ClusterChosenSerializer(serializers.ModelSerializer):
    cluster_1_r = ClusterSerializer(source = 'cluster_1',read_only = True)
    cluster_2_r = ClusterSerializer(source = 'cluster_2',read_only = True)
    cluster_3_r = ClusterSerializer(source = 'cluster_3',read_only = True)
    class Meta:
        model = ClusterChosen
        exclude = ['student','id']
        extra_kwargs = {'cluster_1': {'write_only': True},'cluster_2': {'write_only': True},'cluster_3': {'write_only': True}}

class StudentSerializer(serializers.ModelSerializer):
    roll = serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='username')
    course_name = serializers.CharField(source = 'course.name',read_only = True)
    course = serializers.PrimaryKeyRelatedField(queryset = Course.objects.all(),write_only = True)
    branch = serializers.StringRelatedField()
    branchFullname = serializers.CharField(source = 'branch.branchFullname',read_only = True)
    branch_write = serializers.PrimaryKeyRelatedField(queryset=Specialization.objects.all(),write_only = True)
    city = serializers.StringRelatedField()
    city_write = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(),write_only = True)
    isBanned = serializers.SerializerMethodField(read_only = True)
    # state = serializers.SlugRelatedField(slug_field='name',read_only = True)
    state = serializers.CharField(source='city.state.name',read_only=True)
    college_email = serializers.CharField(source='roll.email',read_only=True)
    eligibility = serializers.SerializerMethodField()
    class_12_domicile = serializers.SlugRelatedField(queryset = State.objects.all(),slug_field='name')
    
    def get_eligibility(self,item):
        result = {}
        try:
            course_year = CourseYearAllowed.objects.get(course=item.course,year=item.current_year)
        except CourseYearAllowed.MultipleObjectsReturned:
            raise APIException("Details of multiple CourseYears present with same type")
        except CourseYearAllowed.DoesNotExist:
            raise APIException("CourseYear does not exist in CourseYearAllowed Table")

        result["allowed_for"] = course_year.type_allowed
        if result["allowed_for"] == "placement" or result["allowed_for"] == "both":
            try:
                ns = StudentNotSitting.objects.get(student = item)
            except StudentNotSitting.DoesNotExist:
                result["sitting"] = True
                return result
            result["sitting"] = False
            result["reason"] = StudentNotSittingSerializer(ns).data["reason"]
        elif result["allowed_for"] == "intern":
            intern = StudentIntern.objects.get(student = item)
            data = StudentInternSerializer(intern).data
            result["resume"] = data["resume"]

        return result

    def get_isBanned(self,item):
        return (item.banned_date < timezone.now() and item.over_date > timezone.now())

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        branch = validated_data["branch_write"]
        validated_data.pop('branch_write')
        city = validated_data["city_write"]
        validated_data.pop('city_write')
        student = Student(branch=branch,city = city,**validated_data)
        student.save()
        return student

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.middle_name = validated_data.get('middle_name',instance.middle_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.personal_email = validated_data.get('personal_email',instance.personal_email)
        instance.gender =  validated_data.get('gender',instance.gender)
        instance.pnumber = validated_data.get('pnumber',instance.pnumber)
        instance.dob = validated_data.get('dob',instance.dob)
        instance.current_year = validated_data.get('current_year',instance.current_year)
        instance.category = validated_data.get('category',instance.category)
        instance.cgpi = validated_data.get('cgpi',instance.cgpi)
        instance.gate_score = validated_data.get('gate_score',instance.gate_score)
        instance.cat_score = validated_data.get('cat_score',instance.cat_score)
        instance.class_10_year = validated_data.get('class_10_year',instance.class_10_year)
        instance.class_10_perc = validated_data.get('class_10_perc',instance.class_10_perc)
        instance.class_12_year = validated_data.get('class_12_year',instance.class_12_year)
        instance.class_12_perc = validated_data.get('class_12_perc',instance.class_12_perc)
        instance.active_backlog = validated_data.get('active_backlog',instance.active_backlog)
        instance.total_backlog = validated_data.get('total_backlog',instance.total_backlog)
        instance.linkedin = validated_data.get('linkedin',instance.linkedin)
        instance.save()
        return instance


class StudentTPOSerializer(StudentSerializer):
    isNotSitting = serializers.SerializerMethodField(read_only = True)
    isPlaced = serializers.SerializerMethodField(read_only = True)
    countPlacement = serializers.SerializerMethodField(read_only = True)
    placedClusters = serializers.SerializerMethodField(read_only = True)

    def get_isNotSitting(self, item):
        try:
            item.student_ns
        except:
            return False
        return True

    def get_countPlacement(self, item):
        student_placement = None
        try:
            student_placement = item.student_placement
        except:
            return 0

        placed = None
        try:
            placed = Placed.objects.get(student = student_placement)
        except Placed.DoesNotExist:
            return 0
        except Placed.MultipleObjectsReturned:
            return len(placed)
        return 1

    def get_isPlaced(self,item):
        return (self.get_countPlacement(item)>0)

    def get_placedClusters(self, item):
        student_placement = None
        try:
            student_placement = item.student_placement
        except:
            return []

        chosenclusters = None
        try:
            chosenclusters = student_placement.cluster
        except:
            return "Clusters were not chosen by you!! Please select your clusters and then come back"

        placed = Placed.objects.filter(student = student_placement)
        clusters_list = []
        for placement in placed:
            obj = {}
            cluster = Cluster.objects.get(starting__lt = placement.job_role.ctc,ending__gte = placement.job_role.ctc)

            obj['cluster'] = cluster.cluster_id
            if cluster.cluster_id < chosenclusters.cluster_1.cluster_id:
                obj['type'] = "below"
            elif cluster.cluster_id == chosenclusters.cluster_1.cluster_id:
                obj['type'] = "base"
            elif cluster.cluster_id > chosenclusters.cluster_1.cluster_id and cluster.cluster_id < chosenclusters.cluster_2.cluster_id:
                obj['type'] = "above_base"
            elif cluster.cluster_id == chosenclusters.cluster_2.cluster_id:
                obj['type'] = "middle"
            elif cluster.cluster_id > chosenclusters.cluster_2.cluster_id and cluster.cluster_id < chosenclusters.cluster_3.cluster_id:
                obj['type'] = "above_middle"
            elif cluster.cluster_id == chosenclusters.cluster_3.cluster_id:
                obj['type'] = "dream"
            clusters_list.append(obj)
        # print(clusters_list)
        return clusters_list


class StudentPlacementSerializer(serializers.ModelSerializer):
    # student = StudentSerializer(read_only = True)
    student = serializers.CharField(source = 'student.roll.username')
    cluster = ClusterChosenSerializer()
    roll = serializers.CharField(write_only = True)

    class Meta:
        model = StudentPlacement
        fields = '__all__'

    def create(self,validated_data):
        print(validated_data)
        cluster_1 = validated_data["cluster"].get('cluster_1')
        cluster_2 = validated_data["cluster"].get('cluster_2')
        cluster_3 = validated_data["cluster"].get('cluster_3')
        validated_data.pop('cluster')
        resume = validated_data.get("resume")
        undertaking = validated_data.get("undertaking")
        roll = validated_data.pop('roll')
        student = Student.objects.get(roll__username = roll)

        student_placement = StudentPlacement(student = student,resume = resume,undertaking = undertaking)

        student_placement.save()

        cluster_chosen = ClusterChosen(student = student_placement,cluster_1 =  cluster_1,cluster_2 = cluster_2,cluster_3 = cluster_3)

        cluster_chosen.save()

        return student_placement


class StudentInternSerializer(serializers.ModelSerializer):
    # student = StudentSerializer(read_only = True)
    student = serializers.CharField(source = 'student.roll.username')

    roll = serializers.CharField(write_only = True)
    class Meta:
        model = StudentIntern
        fields = ['student','resume','roll']

    def create(self,validated_data):
        print(validated_data)
        roll = validated_data.pop("roll")
        validated_data.pop("student")
        # owner = validated_data.pop("owner")
        student_id = Student.objects.get(roll__username = roll)
        intern_student = StudentIntern(student = student_id,**validated_data)
        intern_student.save()
        return intern_student

class StudentNotSittingSerializer(serializers.ModelSerializer):
    # student = StudentSerializer(read_only = True)
    student = serializers.CharField(source = 'student.roll.username')
    roll = serializers.CharField(write_only = True)

    class Meta:
        model = StudentNotSitting
        fields = '__all__'

    def create(self,validated_data):
        # owner = validated_data.pop("owner")
        roll = validated_data.pop("roll")
        validated_data.pop("student")

        student_id = Student.objects.get(roll__username = roll)
        not_sitting_student = StudentNotSitting(student = student_id,**validated_data)
        not_sitting_student.save()
        return not_sitting_student


class Check(serializers.RelatedField):
    def to_representation(self, value):
        print(value)
        return value.student.course.name + value.student.branch.branchName+str(value.student.passing_year)
class Check_rol(serializers.RelatedField):
    def to_representation(self, value):
        return value.drive.session

class PlacedSerializer(serializers.ModelSerializer):
    # student =  Check(read_only = True)
    # job_role = Check_rol(read_only = True)
    class Meta:
        model = Placed
        fields = '__all__'

class InternedSerializer(serializers.ModelSerializer):
    # student =  Check(read_only = True)
    # job_role = Check_rol(read_only = True)
    btech = serializers.CharField(source = 'student.student.course.name')
    company_name = serializers.CharField(source = 'job_role.drive.company.name')
    class Meta:
        model = Interned
        fields = '__all__'