from rest_framework import serializers
from .models import GeneralAnnouncement, CompanyAnnouncement, Resources
from drive.models import Drive

class GeneralAnnouncementSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = GeneralAnnouncement
        fields = '__all__'
    def get_image_url(self,obj):
        return "https://picsum.photos/100"
    
class CompanyAnnouncementSerializer(serializers.ModelSerializer):
    drive = serializers.PrimaryKeyRelatedField(queryset=Drive.objects.all(), write_only=True)
    company_name = serializers.CharField(source='drive.company.name', read_only=True)
    job_type = serializers.CharField(source='drive.job_type', read_only=True)
    session = serializers.CharField(source='drive.session', read_only=True)
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = CompanyAnnouncement
        fields = '__all__'
    def get_image_url(self,obj):
        return "https://picsum.photos/100"
    

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = "__all__"