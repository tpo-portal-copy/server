from rest_framework import serializers
from student.models import Student 
from company.models import Company
from .models import Role,Experience

class StudentListingField(serializers.RelatedField):
    def to_representation(self, value):
        return value.roll.username

    def to_internal_value(self, value):
        print(Student.objects.get(roll__username = value))
        return Student.objects.get(roll__username = value)


class ExperienceSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    # student = serializers.SlugRelatedField(queryset = Student.objects.all(),slug_field='roll')
    student = StudentListingField(queryset = Student.objects.all())
    roles = serializers.SlugRelatedField(queryset = Role.objects.all(),slug_field='role')
    class Meta:
        model = Experience
        fields = '__all__'

    def create(self,validated_data):
        experience = Experience(**validated_data)
        experience.save()
        return experience

        