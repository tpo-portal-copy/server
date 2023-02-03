from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from course.models import *
from django.db.models import Q

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
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    roll = UserSerializer()
    course = CourseSerializer()
    branch = BranchSerializer()
    city = CitySerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        
        user_data  = list(validated_data.pop('roll').items())
        course_data  = list(validated_data.pop('course').items())
        branch_data = list(validated_data.pop('branch').items())
        city_data = list(validated_data.pop('city').items())


        user = User.objects.get(username = user_data[0][1])
        course = Course.objects.get(name = course_data[0][1])
        branch = Specialization.objects.get(Q( branch_name = branch_data[0][1]) & Q(course = course))
        city = City.objects.get(name = city_data[0][1])

        student = Student(roll = user,course = course,branch = branch,city = city,**validated_data)
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

class ClusterChosenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterChosen
        exclude = ['student','id']


class StudentPlacementSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only = True)
    cluster = ClusterChosenSerializer(required = False)

    class Meta:
        model = StudentPlacement
        fields = '__all__'

    def create(self,validated_data):
        cluster_1 = validated_data["cluster"].get('cluster_1')
        cluster_2 = validated_data["cluster"].get('cluster_2')
        cluster_3 = validated_data["cluster"].get('cluster_3')
        validated_data.pop('cluster')
        resume = validated_data.get("resume")
        undertaking = validated_data.get("undertaking")

        student_username = validated_data['student'].get('roll').get('username')

        student = Student.objects.get(roll__username = student_username)

        student_placement = StudentPlacement(student = student,resume = resume,undertaking = undertaking)

        student_placement.save()

        cluster_chosen = ClusterChosen(student = student_placement,cluster_1 =  cluster_1,cluster_2 = cluster_2,cluster_3 = cluster_3)

        cluster_chosen.save()

        return student_placement




        


class StudentInternSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only = True)
    class Meta:
        model = StudentIntern
        fields = '__all__'

    def create(self,validated_data):
        owner = validated_data.pop("owner")
        student_id = Student.objects.get(roll__username = owner)
        intern_student = StudentIntern(student = student_id,**validated_data)
        intern_student.save()
        return intern_student

class StudentNotSittingSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only = True)
    class Meta:
        model = StudentNotSitting
        fields = '__all__'

    def create(self,validated_data):
        owner = validated_data.pop("owner")
        student_id = Student.objects.get(roll__username = owner)
        not_sitting_student = StudentNotSitting(student = student_id,**validated_data)
        not_sitting_student.save()
        return not_sitting_student

    


        



        
        
      
