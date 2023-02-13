from rest_framework import serializers
from .models import *
from company.models import JNF_placement,JNF_intern,Company
from course.models import Specialization,Course
from course.serializers import SpecialisationSerializer

class DriveSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset =Company.objects.all(),slug_field="name")
    eligible_batches = SpecialisationSerializer(many = True)

    class Meta:
        model = Drive
        fields = '__all__'
        # exclude = ['job_desc']

    def create(self,validated_data):
        name = validated_data["company"]
        eligible_batches = validated_data.pop("eligible_batches")
        # print(eligible_batches)
        # validated_data["job_desc"] = name.name+validated_data["name"]

        drive = Drive(**validated_data)
        drive.save()

        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branch_name = batches["branch_name"])
            drive.eligible_batches.add(specialization)
        return drive

    def update(self, instance, validated_data):
        name = validated_data["company"]
        validated_data["job_desc"] = name.name+validated_data["name"]
        instance.company = validated_data.get('company',instance.company)
        instance.ctc_offered = validated_data.get('ctc_offered',instance.ctc_offered)
        instance.name = validated_data.get('name',instance.name)
        instance.job_desc = validated_data.get('job_desc',instance.job_desc)
        instance.starting_date = validated_data.get('starting_date',instance.starting_date)
        instance.year = validated_data.get('year',instance.year)
        instance.job_type = validated_data.get('job_type',instance.job_type)
        eligible_batches = validated_data.get('eligible_batches')
        
        new_batches = []
        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branch_name = batches["branch_name"])
            new_batches.append(specialization)


        instance.eligible_batches.set(new_batches)

        instance.save()
        return instance



    
        

    