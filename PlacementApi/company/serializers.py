from rest_framework import serializers
from .models import Company, HR_details, JNF, JNF_placement, JNF_intern, JNF_intern_fte
from course.models import Specialization
from course.serializers import SpecialisationSerializer
from django.core.exceptions import FieldDoesNotExist

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    def update(self, instance, validated_data):
        print(instance.logo)
        storage, path = instance.logo.storage, instance.logo.path
        storage.delete(path)
        return super().update(instance, validated_data)


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
    eligibleBatches = SpecialisationSerializer(many = True)
    class Meta:
        model = JNF_placement
        fields = '__all__'

    # def to_representation(self, instance):
    #     """
    #     Overwrites choices fields to return their display value instead of their value.
    #     """
    #     data = super().to_representation(instance)
    #     for field in data:
    #         try:
    #             if instance._meta.get_field(field).choices:        
    #                 data[field] = getattr(instance, "get_" + field + "_display")()
    #         except FieldDoesNotExist:
    #             pass
    #     return data

    def create(self, validated_data):
        eligible_batches = validated_data.pop("eligibleBatches")
        # print(eligible_batches)

        jnf = JNF_placement(**validated_data)
        jnf.save()

        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branchName = batches["branchName"])
            jnf.eligible_batches.add(specialization)
        return jnf

    def update(self, instance, validated_data):
        instance.jnf = validated_data.get('jnf',instance.jnf)
        instance.tentativeJoiningDate = validated_data.get('tentativeJoiningDate',instance.tentativeJoiningDate)
        instance.jobProfile = validated_data.get('jobProfile',instance.jobProfile)
        instance.ctc = validated_data.get('ctc',instance.ctc)
        # instance.session = validated_data.get('session',instance.session)

        eligible_batches = validated_data.get('eligibleBatches')
        
        new_batches = []
        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branchName = batches["branchName"])
            new_batches.append(specialization)


        instance.eligible_batches.set(new_batches)

        instance.save()
        return instance


class JNFInternFTESerializer(serializers.ModelSerializer):
    jnf = JnfRelatedfield(queryset = JNF.objects.all())
    eligibleBatches = SpecialisationSerializer(many = True)
    class Meta:
        model = JNF_intern_fte
        fields = '__all__'

    # def to_representation(self, instance):
    #     """
    #     Overwrites choices fields to return their display value instead of their value.
    #     """
    #     data = super().to_representation(instance)
    #     for field in data:
    #         try:
    #             if instance._meta.get_field(field).choices:        
    #                 data[field] = getattr(instance, "get_" + field + "_display")()
    #         except FieldDoesNotExist:
    #             pass
    #     return data

    def create(self, validated_data):
        eligible_batches = validated_data.pop("eligibleBatches")

        jnf = JNF_intern_fte(**validated_data)
        jnf.save()

        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branchName = batches["branchName"])
            jnf.eligible_batches.add(specialization)
        return jnf

    def update(self, instance, validated_data):
        instance.jnf = validated_data.get('jnf',instance.jnf)
        instance.tentativeJoiningDate = validated_data.get('tentativeJoiningDate',instance.tentativeJoiningDate)
        instance.jobProfile = validated_data.get('jobProfile',instance.jobProfile)
        instance.ctc = validated_data.get('ctc',instance.ctc)

        eligible_batches = validated_data.get('eligible_batches')
        
        new_batches = []
        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branchName = batches["branchName"])
            new_batches.append(specialization)

        instance.eligible_batches.set(new_batches)

        instance.save()
        return instance

class JNFInternSerializer(serializers.ModelSerializer):
    # jnf = JNFSerializer()
    # jnf = serializers.StringRelatedField()
    jnf = JnfRelatedfield(queryset = JNF.objects.all())
    duration = serializers.ChoiceField(choices=[(1,"One Month"), (2, "Two Months")])
    eligibleBatches = SpecialisationSerializer(many = True)
    class Meta:
        model = JNF_intern
        fields = '__all__'

    # def to_representation(self, instance):
    #     """
    #     Overwrites choices fields to return their display value instead of their value.
    #     """
    #     data = super().to_representation(instance)
    #     for field in data:
    #         try:
    #             if instance._meta.get_field(field).choices:        
    #                 data[field] = getattr(instance, "get_" + field + "_display")()
    #         except FieldDoesNotExist:
    #             pass
    #     return data

    def create(self, validated_data):
        eligible_batches = validated_data.pop("eligibleBatches")
        # print(eligible_batches)

        jnf = JNF_intern(**validated_data)
        jnf.save()

        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branchName = batches["branchName"])
            jnf.eligible_batches.add(specialization)
        return jnf
        # return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.jnf = validated_data.get('jnf',instance.jnf)
        instance.jobProfile = validated_data.get('jobProfile',instance.jobProfile)
        instance.ctc = validated_data.get('ctc',instance.ctc)
        instance.hasPpo = validated_data.get('hasPpo',instance.hasPpo)
        instance.duration = validated_data.get('duration',instance.duration)
        instance.tentativeJoiningDate = validated_data.get('tentativeJoiningDate',instance.tentativeJoiningDate)

        eligible_batches = validated_data.get('eligibleBatches')
        
        new_batches = []
        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branchName = batches["branchName"])
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


class JNF_TPO_Serializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    class Meta:
        model = JNF
        fields = ['id', 'company', 'session', 'isPlacement', 'isIntern', 'isSixMonthsIntern', 'modeOfHiring', 'tentativeDriveDate', 'isApproved']


class JNFSerializer(serializers.ModelSerializer):
    # company = CompanySerializer()
    company = serializers.SlugRelatedField(queryset = Company.objects.all(),slug_field='name')
    jnfPlacement = JNFPlacementSerializer(read_only = True,required = False, many = True)
    jnfIntern = JNFInternSerializer(read_only = True,required = False, many = True)
    jnfInternFte = JNFInternFTESerializer(read_only = True,required = False, many = True)
    hr = serializers.SerializerMethodField()
    def get_hr(self,item):
        # print(type(item))
        # print(item.company)
        HR_s = HR_details.objects.filter(company__name=item.company)
        return HRSerializer(HR_s, many=True).data
    class Meta:
        model = JNF
        fields = '__all__'

    def create(self, validated_data):
        jnf = JNF(**validated_data)
        jnf.save()

        # print(new_hr)
        # jnf.hr.set(new_hr)

        # validated_data['hr'] = new_hr
        # return jnf

        return jnf
    # def update(self, instance, validated_data):
    #     instance.jnf = validated_data.get('jnf',instance.jnf)