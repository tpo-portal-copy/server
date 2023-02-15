from django.shortcuts import render
from rest_framework import generics
# from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Drive, Role
from company.models import JNF_intern
from .serializers import DriveSerializer,JobRolesSerializer
from student.pagination import CustomPagination
from rest_framework.exceptions import APIException
from rest_framework.response import Response
# Create your views here.


class DriveList(generics.ListCreateAPIView):
    # queryset = Drive.objects.select_related('company')
    queryset = Drive.objects.all()
    serializer_class = DriveSerializer
    # filter_backends = (filters.DjangoFilterBackend)
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        print(request.data)
        for new_role in request.data["other"]:
            Role.objects.get_or_create(name=new_role)
        
        driveserializer = DriveSerializer(data = request.data)
        if driveserializer.is_valid():
            drive = driveserializer.save()
            job_roles = request.data["job_roles"]
            for job_role in job_roles:
                new_role = JobRolesSerializer(data={"drive":drive.pk,"role":job_role["role"],"ctc":job_role["ctc"], "cgpi":float(job_role["cgpi"]),"eligible_batches":job_role['eligible_batches']})
                if(new_role.is_valid()):
                    new_role.save()
                else:
                    print(new_role.errors)
                    print("Invalid Data for Job Role")
            return Response(driveserializer.data)
        else:
            raise APIException("Invalid Data for Drive")

class DriveDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drive.objects.select_related('company')
    serializer_class = DriveSerializer

    