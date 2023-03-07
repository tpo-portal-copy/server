from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import status
# from course.models import CourseYearAllowed
from .filters import StudentPlacementFilter,StudentInternFilter,StudentNSFilter,StudentFilter,PPOFilter
from .pagination import CustomPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Max,Count,Avg,Min
from django.db.models import F
from experience.models import Experience
from rest_framework import filters
class RouteList(APIView):
    def get(self,request):
        routes = {'student/' : "to get list of students basic info",
                  'student/<str:pk>' : "this will give data of specific student also used for create , update and delete",
                  'student/detailplacement/' : 'to get list of students placement info',
                  'student/detailplacement/<str:pk>' : "this will give data of specific student placement  also used for create , update and delete",
                  'student/detailintern/':"to get list of students placement info",
                  'student/detailintern/<str:pk>':"this will give data of specific student intern also used for create , update and delete",
                  'student/detailnositting/':"to get list of students who are not sitting in placement info",
                  'student/detailintern/<str:pk>':"this will give data of specific student not sitting also used for create , update and delete"}

        return Response(routes)

class PPOList(generics.ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    queryset = PPO.objects.all() 
    serializer_class = PPOSerializer
    filterset_class = PPOFilter
    pagination_class = CustomPagination

           

class StudentList(APIView):
    pagination_class = CustomPagination
    filter_class = StudentFilter
    
    def get(self,request):
        queryset = Student.objects.select_related('roll').all()
        queryset = self.filter_class(request.query_params,queryset).qs
        queryset = queryset.order_by('cgpi')
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        serialized_data = StudentSerializer(queryset,many = True)
        return paginator.get_paginated_response(serialized_data.data)

    def post(self,request): 
        new_student = StudentSerializer(data = request.data)
        
        if new_student.is_valid():
            new_student.save()    
            return Response(new_student.data,status=status.HTTP_201_CREATED)
        else:
            print(request.data)
        
        print(new_student.errors)
        return Response(new_student.errors,status=status.HTTP_400_BAD_REQUEST)

class StudentDetail(APIView):
    
    def get(self,request,pk):
        students = Student.objects.get(roll__username=pk)
        serialized_data = StudentSerializer(students)
        return Response(serialized_data.data)

    def put(self,request,pk):
        student = Student.objects.get(roll__username = pk)
        update_student = StudentSerializer(instance=student,data = request.data)
        if update_student.is_valid():
            update_student.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(update_student.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        student = Student.objects.get(roll__username = pk)
        print(student)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StudentPlacementList(APIView):
    pagination_class = CustomPagination
    filter_class = StudentPlacementFilter
    def get(self,request):
        queryset = StudentPlacement.objects.select_related('student').all()
        queryset = queryset.prefetch_related('cluster').all()

        queryset = self.filter_class(request.query_params,queryset).qs
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        serialized_data = StudentPlacementSerializer(queryset,many = True)
        return paginator.get_paginated_response(serialized_data.data)
        # serialized_data = StudentPlacementSerializer(queryset,many = True)
        # return Response(serialized_data.data)

    def post(self,request):

        new_student_placement = StudentPlacementSerializer(data = request.data)
        # print(request.data)
        if new_student_placement.is_valid():
            new_student_placement.save()   
            return Response(status=status.HTTP_201_CREATED)
        # print(new_student_placement.errors)
        return Response(new_student_placement.errors,status=status.HTTP_400_BAD_REQUEST)

class StudentPlacementDetail(APIView):

    def get(self,request,pk):
        # roll = Student.objects.get(roll__username = pk)
        student_placement = StudentPlacement.objects.get(student__roll__username = pk )
        # students = StudentPlacement.objects.get(student = roll)
        serialized_data = StudentPlacementSerializer(student_placement)
        return Response(serialized_data.data)

    def put(self,request,pk):
        student_placement = StudentPlacement.objects.get(student__roll__username = pk)
        update_student_placememt = StudentPlacementSerializer(instance=student_placement,data = request.data)
        if update_student_placememt.is_valid():
            update_student_placememt.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(update_student_placememt.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        student_placement = StudentPlacement.objects.get(student__roll__username = pk)
        student_placement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StudentInternList(APIView):
    filter_class = StudentInternFilter
    pagination_class = CustomPagination
    def get(self,request):
        queryset = StudentIntern.objects.select_related('student')
        queryset = self.filter_class(request.query_params,queryset).qs
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        serialized_data = StudentInternSerializer(queryset,many = True)
        return paginator.get_paginated_response(serialized_data.data)
        # serialized_data = StudentInternSerializer(queryset,many = True)
        # return Response(serialized_data.data)

    def post(self,request):
        new_student_intern = StudentInternSerializer(data = request.data)
        if new_student_intern.is_valid():
            new_student_intern.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(new_student_intern.errors,status=status.HTTP_400_BAD_REQUEST)



class StudentInternDetail(APIView):
    def get(self,request,pk):
        student_intern = StudentIntern.objects.get(student__roll__username = pk )
        serialized_data = StudentInternSerializer(student_intern)
        return Response(serialized_data.data)

    def put(self,request,pk):
        student_intern= StudentIntern.objects.get(student__roll__username = pk)
        update_student_intern = StudentInternSerializer(instance=student_intern,data = request.data)
        if update_student_intern.is_valid():
            update_student_intern.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(update_student_intern.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        student_intern = StudentIntern.objects.get(student__roll__username = pk)
        student_intern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class StudentNotSittingList(APIView):
    filter_class = StudentNSFilter
    pagination_class = CustomPagination
    def get(self,request):
        queryset = StudentNotSitting.objects.select_related('student')
        queryset = self.filter_class(request.query_params,queryset).qs
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        serialized_data = StudentInternSerializer(queryset,many = True)
        return paginator.get_paginated_response(serialized_data.data)

    def post(self,request):
        new_student_ns = StudentNotSittingSerializer(data = request.data)
        if new_student_ns.is_valid():
            new_student_ns.save() #owner = request.user    
            return Response(status=status.HTTP_201_CREATED)
        return Response(new_student_ns.errors,status=status.HTTP_400_BAD_REQUEST)



class StudentNotSittingDetail(APIView):
    def get(self,request,pk):
        student_NS = StudentNotSitting.objects.get(student__roll__username = pk )
        serialized_data = StudentNotSittingSerializer(student_NS)
        return Response(serialized_data.data)

    def put(self,request,pk):
        student_ns= StudentNotSitting.objects.get(student__roll__username = pk)
        update_student_ns = StudentNotSittingSerializer(instance=student_ns,data = request.data)
        if update_student_ns.is_valid():
            update_student_ns.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(update_student_ns.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        student_ns = StudentNotSitting.objects.get(student__roll__username = pk)
        student_ns.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class StudentPlaced(generics.ListCreateAPIView):
    queryset = Interned.objects.all()
    serializer_class = InternedSerializer
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = InternedSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
        return Response({'sumit' : "yes"})






    


# class clusterchoosen(APIView):
#     def get(self,request):
#         queryset = ClusterChosen.objects.all()
#         seriallized = ClusterChosenSerializer(queryset,many = True)
#         return Response(seriallized.data)



class BasicStats(APIView):
    def get(self,request):
        session = request.query_params["session"]
        # session = "2022-23"
        jtype = request.query_params["type"]
        passingYear = "20" + session[5:]
        passingYear = int(passingYear)
        print(passingYear)
        
        statsInfo = []
        result = {}
        

        if jtype == "intern":
            topCompanies = Interned.objects.filter(drive__session = session).values(name = F('drive__company__name'),logo = F('drive__company__logo')).annotate(max_stipend = Max('job_role__ctc')).order_by('-job_role__ctc')[:10]#student__student__passing_year 
            companiesVisited = Interned.objects.filter(drive__session = session).values(name = F('drive__company__name')).count() 
            # totalStudent = Interned.objects.filter(drive__session = session).values('student').count()
            courseWise = Interned.objects.filter(drive__session = session).values(course =F('student__student__course__name'),branch = F('student__student__branch__branch_name')).annotate(offers = Count('student'),avg_stipend = Avg('job_role__ctc'),max_stipend = Max("job_role__ctc"),min_stipend = Min("job_role__ctc"))
            offers = Interned.objects.filter(student__student__passing_year = passingYear+1).count()
            totalAppeared = StudentIntern.objects.filter(student__passing_year = passingYear+1).count()
            course = Course.objects.count()
            serializer = []
            for company in topCompanies:
                serializer.append(company)
            value = [totalAppeared,offers,companiesVisited,course]
            label = ["Student Appeared","Offers","Companies Visited","Courses"]

            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
            result["topCompanies"] = serializer
            result["basicStats"] = courseWise

        elif jtype == "placement":
            topCompanies = Placed.objects.filter(student__student__passing_year = passingYear).values(name = F('drive__company__name'),logo = F('drive__company__logo')).annotate(max_ctc = Max('job_role__ctc')).order_by('-job_role__ctc')[:10]
            companiesVisited =  Placed.objects.filter(student__student__passing_year = passingYear).values(name = F('drive__company__name')).count()
            # totalStudent = Placed.objects.filter(drive__session = session).values('student').count()
            courseWise = Placed.objects.filter(drive__session = session).values(course =F('student__student__course__name'),branch = F('student__student__branch__branch_name')).annotate(offer = Count('student'),avg_stipend = Avg('job_role__ctc'),max_stipend = Max("job_role__ctc"),min_stipend = Min("job_role__ctc"))

            offers = Placed.objects.filter(student__student__passing_year = passingYear).count()
            totalAppeared = StudentPlacement.objects.filter(student__passing_year = passingYear).count() 
            course = Course.objects.count()
            
            serializer = []
            for company in topCompanies:
                serializer.append(company)
            value = [totalAppeared,offers,companiesVisited,course]
            label = ["Student Appeared","Offers","Companies Visited","courses"]

            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
            result["topCompanies"] = serializer
            result["basicStats"] = courseWise


        else:
            studentReceivedPPO = PPO.objects.filter(student__passing_year = passingYear).values('student').count()
            companiesVisited = PPO.objects.filter(student__passing_year = passingYear).values('company').count()
            offers = PPO.objects.filter(student__passing_year = passingYear).count()
            course = Course.objects.all().count()
            value = [studentReceivedPPO,offers,companiesVisited,course]
            label = ["Student Appeared","Offers","Companies Visited","Courses"]

            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
        return Response(result)


class CommonQueries(APIView):
    pagination_class = CustomPagination

    def get(self,request):
        session = request.query_params["session"]
        jtype = request.query_params["type"]
        order = request.query_params["order"]
      
        name = request.query_params["company"]
        # name = 'inc'
        passingYear = "20" + session[5:]
        if order == "ctc":
            if jtype == "intern":
                queryset = Interned.objects.filter(student__student__passing_year = passingYear,drive__company__name__icontains = name).values(name = F('drive__company__name')).annotate(max_stipend = Max('job_role__ctc')).order_by('-job_role__ctc')

            else:
                queryset = Placed.objects.filter(student__student__passing_year = passingYear,drive__company__name__icontains = name).values(name = F('drive__company__name')).annotate(max_ctc = Max('job_role__ctc')).order_by('-job_role__ctc')
            paginator = self.pagination_class()
            queryset = paginator.paginate_queryset(queryset,request)
            return paginator.get_paginated_response(queryset) 

        else:
            if jtype == "intern":
                queryset = Interned.objects.filter(student__student__passing_year = passingYear,drive__company__name__icontains = name).values(name = F('drive__company__name')).annotate(offers = Count('student')).order_by('-offers')
            else:
                queryset = Placed.objects.filter(student__student__passing_year = passingYear,drive__company__name__icontains = name).values(name = F('drive__company__name')).annotate(offers = Count('student')).order_by('-offers')
            paginator = self.pagination_class()
            queryset = paginator.paginate_queryset(queryset,request)
            return paginator.get_paginated_response(queryset) 

        

    


    ########################## Dashboard API 
class RecentNotifications(APIView):
    def get(self,request):
        result = {}
        driveUpcoming = Drive.objects.all().order_by('-starting_date')[:5]
        recentExperience = Experience.objects.all().order_by('-created_at')[:5]
        print(driveUpcoming)
        serializerdrive = []
        for drive in driveUpcoming:
           serializerdrive.append({'Id' : drive.id,'Company':drive.company.name,'Starting_Date':drive.starting_date})
        result["Drive_Upcoming"] = serializerdrive

        serializerexperience = []
        for exp in recentExperience:
            serializerexperience.append({'Id' : exp.id,'Name':exp.student.first_name,'Created_Date':exp.created_at})
        result["Recent_Experience"] = serializerexperience
        

        return Response(result)

    


            



        
   

            

        

        

        

        
            



