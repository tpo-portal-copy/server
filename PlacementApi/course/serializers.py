from rest_framework import serializers
from .models import Course, Specialization

class SpecialisationSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(queryset = Course.objects.all(),slug_field="name")
    class Meta:
        model = Specialization
        fields = '__all__'