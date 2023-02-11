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


class JnfRelatedfield(serializers.RelatedField):
    def to_representation(self, value):
        return value.company.name
    def to_internal_value(self, data):
        print(data)
        return JNF.objects.get(company__name = data)


class JNFPlacementSerializer(serializers.ModelSerializer):
    # jnf = JNFSerializer()
    # jnf = serializers.StringRelatedField()
    jnf = JnfRelatedfield(queryset = JNF.objects.all())
    eligible_batches = SpecialisationSerializer(many = True)
    class Meta:
        model = JNF_placement
        fields = '__all__'

    def create(self, validated_data):
        eligible_batches = validated_data.pop("eligible_batches")
        # print(eligible_batches)

        jnf = JNF_placement(**validated_data)
        jnf.save()

        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branch_name = batches["branch_name"])
            jnf.eligible_batches.add(specialization)
        return jnf

    def update(self, instance, validated_data):
        instance.jnf = validated_data.get('jnf',instance.jnf)
        instance.tentative_start = validated_data.get('tentative_start',instance.tentative_start)
        instance.job_profile = validated_data.get('job_profile',instance.job_profile)
        instance.ctc = validated_data.get('ctc',instance.ctc)
        # instance.session = validated_data.get('session',instance.session)

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
    # jnf = serializers.StringRelatedField()
    jnf = JnfRelatedfield(queryset = JNF.objects.all())
    eligible_batches = SpecialisationSerializer(many = True)
    class Meta:
        model = JNF_intern
        fields = '__all__'

    def create(self, validated_data):
        eligible_batches = validated_data.pop("eligible_batches")
        # print(eligible_batches)

        jnf = JNF_intern(**validated_data)
        jnf.save()

        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branch_name = batches["branch_name"])
            jnf.eligible_batches.add(specialization)
        return jnf
        # return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.jnf = validated_data.get('jnf',instance.jnf)
        instance.job_profile = validated_data.get('job_profile',instance.job_profile)
        instance.ctc = validated_data.get('ctc',instance.ctc)
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

    def validate_duration(self, value):
        if(value <= 0):
            raise serializers.ValidationError('Internship duration must be at least 1 month')
        elif(value > 6):
            raise serializers.ValidationError('Our college does not allow for internship for more than 6 months')

        print(value)
        return value


class JNFSerializer(serializers.ModelSerializer):
    # company = CompanySerializer()
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    jnf_placement = JNFPlacementSerializer(read_only = True,required = False)
    jnf_intern = JNFInternSerializer(read_only = True,required = False)
    # hr = HRSerializer(many = True)
    class Meta:
        model = JNF
        fields = '__all__'

    def create(self, validated_data):
        HRs = validated_data.pop("hr")

        new_hr = []
        for hr in HRs:
            temp_hr = HRSerializer(data = {"company":hr['company'], "type":hr['type'],"name":hr["name"],"mobile":hr['mobile'],"email":hr["email"]})
            if(temp_hr.is_valid()):
                n_hr = temp_hr.save()
                new_hr.append(n_hr)
            else:
                raise serializers.ValidationError("HR_Details in invalid format")

        jnf = JNF(**validated_data)
        jnf.save()

        # print(new_hr)
        # jnf.hr.set(new_hr)

        # validated_data['hr'] = new_hr
        # return jnf

        return jnf
    # def update(self, instance, validated_data):
    #     instance.jnf = validated_data.get('jnf',instance.jnf)