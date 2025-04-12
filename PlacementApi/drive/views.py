from rest_framework import generics,status
from django_filters import rest_framework
from rest_framework import filters,permissions
from rest_framework.decorators import permission_classes
from accounts import permissions as custom_permissions
from course.models import CourseYearAllowed
from .models import Drive, Role ,JobRoles
from .serializers import DriveSerializer,JobRolesSerializer,RoleSerializer
from student.pagination import CustomPagination
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .filters import DriveFilters
from django.utils import timezone
from django.db.models import Q,Prefetch
# Create your views here.
# from rest_framework.views import APIView

class RolesList(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [permissions.IsAuthenticated]
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
    serializer_class = DriveSerializer
    pagination_class = CustomPagination
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = DriveFilters
   
    def get_queryset(self):
        session = None
        curr_date = timezone.now()
        date = timezone.datetime(curr_date.year, 7, 1, tzinfo=timezone.get_current_timezone())
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        if curr_date <= date:
            session = str(curr_date.year-1) + "-"+str(curr_date.year)[2:]
        else:
            session = str(curr_date.year) + "-"+str(curr_date.year+1)[2:]

        if self.request.user.username == "tpo@nith.ac.in":
            queryset = Drive.objects.filter()
            return queryset
        type = CourseYearAllowed.objects.get(course = self.request.user.student.course,year = self.request.user.student.current_year).type_allowed
        if type == "placement": 
            c = self.request.user.student.student_placement.cluster
            clusters = []
            if self.request.query_params["cluster"] == "":
                clusters = [c.cluster_1.cluster_id,c.cluster_2.cluster_id,c.cluster_3.cluster_id]
            else:
                for cl in self.request.query_params["cluster"].split(','):
                    cl = int(cl)
                    if cl in [c.cluster_1.cluster_id,c.cluster_2.cluster_id,c.cluster_3.cluster_id]:
                        clusters.append(cl)
            print([c.cluster_1.cluster_id,c.cluster_2.cluster_id,c.cluster_3.cluster_id],clusters)

            queryset = Drive.objects.filter(Q(session=session),Q(job_type = type) | Q(job_type = 'intern and fte')).order_by('-starting_date') 
            jobroles_prefetch = Prefetch('job_roles',queryset=JobRoles.objects.filter(cluster__cluster_id__in = clusters))
            queryset = queryset.prefetch_related(jobroles_prefetch)
            drive_list = []
            for drive in queryset:
                if drive.job_roles.count() == 0:
                    drive_list.append(drive.id)
            queryset =  queryset.exclude(id__in = drive_list)
        elif type == "intern":
            queryset = Drive.objects.filter(session=session,job_type = type).order_by('-starting_date')  
        else:
            queryset = None

        return queryset 
    
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [permissions.IsAuthenticated(),custom_permissions.PlacementSession()]
    #     elif self.request.method == 'POST':
    #         return [permissions.IsAuthenticated()]
    #     # custom_permissions.TPRPermissions()|custom_permissions.TPOPermissions()
    #     else:
    #         return []

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
                new_role = JobRolesSerializer(data={"drive":drive.pk,"role":job_role["role"],"ctc":job_role["ctc"], "cgpi":float(job_role["cgpi"]),"eligible_batches":job_role['eligibleBatches']})
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
    queryset = Drive.objects.all()
    permission_classes = [permissions.IsAuthenticated,custom_permissions.TPRPermissions] 
    serializer_class = DriveSerializer
    def put(self, request,pk):
        drive = Drive.objects.get(id = pk)
        serializer = DriveSerializer(instance=drive,data = request.data)
        if serializer.is_valid():
            serializer.save()
        # jobRoles = request.data["job_roles"][0]
        # print(request.data)
        jobRoles = request.data["job_roles"]
        # print(jobRoles)
        jobRoles["drive"] = drive.id
        job_roles = JobRoles.objects.get(id = jobRoles["id"])
        serializerRole = JobRolesSerializer(instance=job_roles,data = jobRoles)
        if serializerRole.is_valid():
            print("valid_data")
            serializerRole.save()
            return Response(serializer.data)
        else:
            print(serializerRole.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    