from rest_framework import serializers
from student.models import Student 
from company.models import Company
from .models import Experience
from drive.models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']

class StudentListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.roll.username

    def to_internal_value(self, value):
        # print(Student.objects.get(roll__username = value))
        return Student.objects.get(roll__username = value)


class ExperienceSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    # student = serializers.SlugRelatedField(queryset = Student.objects.all(),slug_field='roll')
    # company = serializers.PrimaryKeyRelatedField(queryset = Company.objects.all()) 
    student = StudentListingField(queryset = Student.objects.all(),write_only = True)
    name = serializers.SerializerMethodField()
    roles = serializers.SlugRelatedField(queryset = Role.objects.all(),slug_field='name')
    # roles = serializers.PrimaryKeyRelatedField(queryset = Role.objects.all())
    description_read = serializers.SerializerMethodField()
    description = serializers.CharField(write_only = True)
    no_of_rounds = serializers.IntegerField(write_only = True)


    class Meta:
        model = Experience
        fields = '__all__'
    def get_name(self,obj):
        result = {}
        if obj.anonymity:
            result = {}
        else:
            print(obj)
            if obj.student.image_url == None:
                result = {'name' : obj.student.first_name+ " " +obj.student.last_name}
            else:
                result = {'name' : obj.student.first_name+ " " +obj.student.last_name,'logo':"https://picsum.photos/200.jpg"}               

        return result
    def get_description_read(self,obj):
        return obj.description[:250]

    def create(self,validated_data):
        print(validated_data)
        experience = Experience(**validated_data)
        experience.save()
        return experience
    

class ExperienceDetailSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    student = StudentListingField(queryset = Student.objects.all(),write_only = True)
    roles = serializers.SlugRelatedField(queryset = Role.objects.all(),slug_field='name')
    linkedin = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = '__all__'

    def get_name(self,obj):
        name = ""
        if obj.student.middle_name:
            name += obj.student.middle_name + " "
        return obj.student.first_name +" " + name + obj.student.last_name
        
    def get_linkedin(self,obj):
        return obj.student.linkedin    