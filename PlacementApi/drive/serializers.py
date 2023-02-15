from rest_framework import serializers
from .models import Role,JobRoles,Drive
from company.models import JNF_placement,JNF_intern,Company,JNF
from course.models import Specialization
from course.serializers import SpecialisationSerializer
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from pathlib import Path
from django.core.files import File


class JobRolesSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(queryset=Role.objects.all(), slug_field="name")
    eligible_batches = SpecialisationSerializer(many= True)
    drive = serializers.PrimaryKeyRelatedField(queryset = Drive.objects.all(),write_only = True)
    class Meta:
        model = JobRoles
        fields = '__all__'
       

    def create(self, validated_data):
        eligible_batches = validated_data.pop("eligible_batches")

        job_role = JobRoles(**validated_data)
        job_role.save()

        for batches in eligible_batches:
            specialization = Specialization.objects.get(course = batches['course'],branch_name = batches["branch_name"])
            job_role.eligible_batches.add(specialization)
        return job_role

class DriveSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset =Company.objects.all(),slug_field="name")
    job_roles = JobRolesSerializer(read_only = True,many = True)

    class Meta:
        model = Drive
        fields = '__all__'

    def validate_job_desc_pdf(self, value):
        print(value)
        return value
    def create(self,validated_data):
        jnf = None
        if validated_data["job_type"] == "intern" or validated_data["job_type"] == "intern and ppo":
            try:
                jnf = JNF_intern.objects.get(jnf__company__name = validated_data["company"])
            except:
                raise serializers.ValidationError("Corresponding intern details not found")
        elif validated_data["job_type"] == "placement":
            try:
                jnf = JNF_placement.objects.get(jnf__company__name = validated_data["company"])
            except:
                pass
                # raise serializers.ValidationError("Corresponding placement details not found")
        # validated_data["job_desc_pdf"] = jnf.job_desc_pdf

       

        drive = Drive(**validated_data)
        drive.save()
        return drive

    def update(self, instance, validated_data):
        name = validated_data["company"]
        # validated_data["job_desc"] = name.name+validated_data["name"]

        instance.company = validated_data.get('company',instance.company)
        instance.ctc_offered = validated_data.get('ctc_offered',instance.ctc_offered)
        instance.mode_of_hiring = validated_data.get('mode_of_hiring',instance.mode_of_hiring)
        instance.pre_placement_talk = validated_data.get('pre_placement_talk',instance.pre_placement_talk)
        instance.aptitude_test = validated_data.get('aptitude_test',instance.aptitude_test)
        instance.technical_test = validated_data.get('technical_test',instance.technical_test)
        instance.group_discussion = validated_data.get('group_discussion',instance.group_discussion)
        instance.personal_interview = validated_data.get('personal_interview',instance.personal_interview)
        instance.no_of_persons_visiting = validated_data.get('no_of_persons_visiting',instance.no_of_persons_visiting)
        instance.job_location = validated_data.get('job_location',instance.job_location)
        instance.starting_date = validated_data.get('starting_date',instance.starting_date)
        instance.job_type = validated_data.get('job_type',instance.job_type)
        instance.ctc = validated_data.get('ctc',instance.ctc)
        instance.session = validated_data.get('session',instance.session)
        job_roles = validated_data.get('job_roles')
        
        new_job_roles = []
        for job_role in job_roles:
            new_role = JobRolesSerializer(data={"role":job_role["role"],"ctc":job_role["ctc"], "cgpi":float(job_role["cgpi"]),"eligible_batches":job_role['eligible_batches']})
            if(new_role.is_valid()):
                instance = new_role.save()
                new_job_roles.append(instance)
            else:
                print(new_role.errors)
                print("Invalid Data for Job Role")


        instance.job_roles.set(new_job_roles)

        instance.save()
        return instance