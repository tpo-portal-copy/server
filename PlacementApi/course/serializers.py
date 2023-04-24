from rest_framework import serializers
from .models import Course, Specialization, CourseYearAllowed

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class SpecialisationSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(queryset = Course.objects.all(),slug_field="name")
    class Meta:
        model = Specialization
        fields = '__all__'
        # read_only_fields = ('onCampus','offCampusPpo','isActive')

class CourseYearAllowedSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(queryset = Course.objects.all(),slug_field="name")
    class Meta:
        model = CourseYearAllowed
        fields = '__all__'