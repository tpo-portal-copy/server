from django.shortcuts import render,HttpResponse
from rest_framework import generics,status
# from rest_framework.response import Response
from django_filters import rest_framework
from rest_framework import filters

from course.models import Specialization
from .models import Drive, Role ,JobRoles
from company.models import JNF_intern
from .serializers import DriveSerializer,JobRolesSerializer,RoleSerializer
from student.pagination import CustomPagination
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .filters import DriveFilters
# Create your views here.
# from rest_framework.views import APIView

class RolesList(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    # def get(self,request):
    #     roles = Role.objects.values_list('name',flat = True)
    #     print(roles)
    #     roles = {"roles":list(roles)}
    #     return Response(roles)
    # def post(self, request):
    #     print(request.data)
    #     roles,created = Role.objects.get_or_create(name=request.data['name'])
    #     print(created)
    #     return Response(status=status.HTTP_201_CREATED)

# class JobRoles(generics.ListCreateAPIView):
#     queryset = JobRoles.objects.all()
#     serializer_class = JobRolesSerializer

#     def post(self,request):
#         # print(request.data)
#         batches = request.data["eligible_batches"][1:-1]
#         batches = batches.split(',')
#         batches = list(map(int, batches))
#         print(batches)
#         batches_list = []
#         for batch in batches:
#             batches_list.append(Specialization.objects.get(pk=batch))
#         print(batches_list)
#         role = Role.objects.get(id=request.data['role'])
#         serializer = JobRolesSerializer(data ={"role":role.name, "drive":request.data['drive'], "ctc":request.data['ctc'], "cgpi":request.data['cgpi'],"eligible_batches" : batches})
#         # serializer = JobRolesSerializer(data =request.data)
#         if serializer.is_valid():
#             print("Valid Data")
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
#         else:
#             print(serializer.errors)
#             return Response(status=status.HTTP_400_BAD_REQUEST)





class DriveList(generics.ListCreateAPIView):
    # queryset = Drive.objects.select_related('company')
    queryset = Drive.objects.prefetch_related('job_roles').order_by('id')
    serializer_class = DriveSerializer
    # filter_backends = (filters.DjangoFilterBackend)
    pagination_class = CustomPagination
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = DriveFilters

    def post(self, request, *args, **kwargs):
        print(request.data)
        if "other" in request.data:    
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
            print(driveserializer.errors)
            raise APIException("Invalid Data for Drive")

class DriveDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drive.objects.select_related('company')
    serializer_class = DriveSerializer
    def put(self, request,pk):
        drive = Drive.objects.get(id = pk)
        serializer = DriveSerializer(instance=drive,data = request.data)
        if serializer.is_valid():
            serializer.save()
        jobRoles = request.data["job_roles"][0]
        jobRoles["drive"] = drive.id
        job_roles = JobRoles.objects.get(id = jobRoles["id"])
        serializerRole = JobRolesSerializer(instance=job_roles,data = jobRoles)
        if serializerRole.is_valid():
            serializerRole.save()
            return Response(serializer.data)
        

    