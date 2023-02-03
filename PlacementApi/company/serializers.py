from rest_framework import serializers
from .models import Company, HR_details

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    def update(self, instance, validated_data):
        print(instance.logo)
        storage, path = instance.logo.storage, instance.logo.path
        storage.delete(path)
        return super().update(instance, validated_data)
    # Field Level Serializer
    def validate_file_size():
        pass

class HRSerializer(serializers.ModelSerializer):
    # company = CompanySerializer()
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    class Meta:
        model = HR_details
        fields = '__all__'