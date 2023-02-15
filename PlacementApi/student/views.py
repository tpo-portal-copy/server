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
from django.db.models import Max,Count
from django.db.models import F
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
        if new_student_placement.is_valid():
            new_student_placement.save()   
            return Response(status=status.HTTP_201_CREATED)
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






    


# class clusterchoosen(APIView):
#     def get(self,request):
#         queryset = ClusterChosen.objects.all()
#         seriallized = ClusterChosenSerializer(queryset,many = True)
#         return Response(seriallized.data)



class BasicStats(APIView):
    pagination_class = CustomPagination
    def get(self,request):
        session = request.query_params["session"]
        jtype = request.query_params["type"]
        passingYear = "20" + session[5:]
        
        result = {}

        if jtype == "intern":
            queryset = Interned.objects.filter(student__student__passing_year = passingYear).values(name = F('drive__company__name')).annotate(max_stipend = Max('job_role__ctc')).order_by('-job_role__ctc')[:5]
            offers = Interned.objects.filter(student__student__passing_year = passingYear).count()
            totalAppeared = StudentIntern.objects.filter(student__passing_year = passingYear).count()
            serializer = []
            for company in queryset:
                serializer.append(company)
            result["offers"] = offers
            result["totalAppeared"] = totalAppeared
            result["companies"] = serializer

        else:
            queryset = Placed.objects.filter(student__student__passing_year = passingYear).values(name = F('drive__company__name')).annotate(max_ctc = Max('job_role__ctc')).order_by('-job_role__ctc')[:5]
            offers = Placed.objects.filter(student__student__passing_year = passingYear).count()
            totalAppeared = StudentPlacement.objects.filter(student__passing_year = passingYear).count() 
            serializer = []
            for company in queryset:
                serializer.append(company)
            result["offers"] = offers
            result["totalAppeared"] = totalAppeared
            result["companies"] = queryset
        
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        return paginator.get_paginated_response(result)


class CommonQueries(APIView):
    pagination_class = CustomPagination
    def get(self,request):
        session = request.query_params["session"]
        jtype = request.query_params["type"]
        order = request.query_params["order"]
        passingYear = "20" + session[5:]
        result = {}
        if order == "ctc":
            queryset = list()
            if jtype == "intern":
                queryset = list(Interned.objects.filter(student__student__passing_year = passingYear).values(name = F('drive__company__name')).annotate(max_stipend = Max('job_role__ctc')).order_by('-job_role__ctc'))

            else:
                queryset =list(Placed.objects.filter(student__student__passing_year = passingYear).values(name = F('drive__company__name')).annotate(max_ctc = Max('job_role__ctc')).order_by('-job_role__ctc'))
            
            serializer = []
            print(queryset)
            for company in queryset:
                serializer.append(company)
            result["companies"] = serializer
        else:
            queryset = list()
            if jtype == "intern":
                queryset = list(Interned.objects.filter(student__student__passing_year = passingYear).values(name = F('drive__company__name')).annotate(offers = Count('student')).order_by('-offers'))
            else:
                queryset = list(Placed.objects.filter(student__student__passing_year = passingYear).values(name = F('drive__company__name')).annotate(offers = Count('student')).order_by('-offers'))
            
            serializer = []
            for company in queryset:
                serializer.append(company)
            result["companies"] = serializer
        
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        return paginator.get_paginated_response(result) 
            



        
   

            

        

        

        

        
            



