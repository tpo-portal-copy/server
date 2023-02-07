from rest_framework import serializers
from .models import Company, HR_details, JNF, JNF_placement, JNF_intern
from course.models import Specialization
from course.serializers import SpecialisationSerializer

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

class JNFSerializer(serializers.ModelSerializer):
    # company = CompanySerializer()
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    class Meta:
        model = JNF
        fields = '__all__'

class JNFPlacementSerializer(serializers.ModelSerializer):
    # jnf = JNFSerializer()
    jnf = serializers.StringRelatedField()
    eligible_batches = SpecialisationSerializer(many = True)
    class Meta:
        model = JNF_placement
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.jnf = validated_data.get('jnf',instance.jnf)
        instance.joining_date_placement = validated_data.get('joining_date_placement',instance.joining_date_placement)
        instance.job_profile = validated_data.get('job_profile',instance.job_profile)
        instance.ctc = validated_data.get('ctc',instance.ctc)
        instance.session = validated_data.get('session',instance.session)

        eligible_batches = validated_data.get('eligible_batches')
        
        new_batches = []
        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branch_name = batches["branch_name"])
            new_batches.append(specialization)


        instance.eligible_batches.set(new_batches)

        instance.save()
        return instance

class JNFInternSerializer(serializers.ModelSerializer):
    # jnf = JNFSerializer()
    jnf = serializers.StringRelatedField()
    eligible_batches = SpecialisationSerializer(many = True)
    class Meta:
        model = JNF_intern
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.jnf = validated_data.get('jnf',instance.jnf)
        instance.job_profile = validated_data.get('job_profile',instance.job_profile)
        instance.ctc = validated_data.get('ctc',instance.ctc)
        instance.session = validated_data.get('session',instance.session)
        instance.has_ppo = validated_data.get('has_ppo',instance.has_ppo)
        instance.duration = validated_data.get('duration',instance.duration)
        instance.tentative_start = validated_data.get('tentative_start',instance.tentative_start)

        eligible_batches = validated_data.get('eligible_batches')
        
        new_batches = []
        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branch_name = batches["branch_name"])
            new_batches.append(specialization)


        instance.eligible_batches.set(new_batches)

        instance.save()
        return instance