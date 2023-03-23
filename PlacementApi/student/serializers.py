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
    branch_fullname = serializers.CharField(source = 'branch.branch_fullname',read_only = True)
    branch_write = serializers.PrimaryKeyRelatedField(queryset=Specialization.objects.all(),write_only = True)
    city = serializers.StringRelatedField()
    city_write = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(),write_only = True)
    isBanned = serializers.SerializerMethodField(read_only = True)
    # state = serializers.SlugRelatedField(slug_field='name',read_only = True)
    state = serializers.SerializerMethodField()
    college_email = serializers.SerializerMethodField()
    eligibility = serializers.SerializerMethodField()
    class_12_domicile = serializers.SlugRelatedField(queryset = State.objects.all(),slug_field='name')
    
    def get_eligibility(self,item):
        result = {}
        try:
            course_year = CourseYearAllowed.objects.get(course=item.course,year=item.current_year)
        except Company.DoesNotExist:
            raise APIException("Error in Company Serializer")
        except CourseYearAllowed.MultipleObjectsReturned:
            new_val = CourseYearAllowed.objects.filter(course=item.course,year=item.current_year)
            print(new_val)
            raise APIException("Details of multiple CourseYears present with same type")
 
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
   
    def get_college_email(self,item):
        return item.roll.email

    def get_state(self,item):
        return item.city.state.name
   
    def get_isBanned(self,item):
       return (item.banned_date < timezone.now() and item.over_date > timezone.now())
    
    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        # validated_data.pop('roll')
        # course = validated_data["course"]
        branch = validated_data["branch_write"]
        validated_data.pop('branch_write')
        # validated_data.pop('branch_write')
        city = validated_data["city_write"]
        validated_data.pop('city_write')
        # state = validated_data.pop('state')
        # branch = Specialization.objects.get(Q(branch_name = branch_data)
        # city = City.objects.get(Q(name = city_data)& Q(state__name = state))
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
        return value.student.course.name + value.student.branch.branch_name+str(value.student.passing_year)
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





        



        
        
      
