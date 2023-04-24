from django.shortcuts import render
from rest_framework import generics, status,views,permissions
from .models import Course, Specialization, CourseYearAllowed
from .serializers import CourseSerializer, SpecialisationSerializer, CourseYearAllowedSerializer
from rest_framework.response import Response
from accounts import permissions as custom_permissions

# Create your views here.
class CourseAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    
class courseAPIViewDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SpecializationAPIView(views.APIView):
    def get(self,request):
        branches = Specialization.objects.all()
        serializer = SpecialisationSerializer(branches,many = True)
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(name = request.data["course"]["name"])
        except Course.DoesNotExist:
            serializer_course = CourseSerializer(data =request.data["course"])
            ### coures year alllowed bhi likhna hai
            if serializer_course.is_valid():
                course = serializer_course.save() 
        for data in request.data["branches"]:
            data["course"] = course.name
            serializer = SpecialisationSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
    def put(self,request):
        course = Course.objects.get(id = request.data["course"]["id"]) # we need id with course
        course_serializer = CourseSerializer(instance=course,data = request.data["course"])
        if course_serializer.is_valid():
           course = course_serializer.save()
        for data in request.data["branches"]:
            data["course"] = course.name
            branch = Specialization.objects.get(id = data["id"])
            serializer = SpecialisationSerializer(instance = branch,data = data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
class SpecializationDetailAPIView(views.APIView):  
    def get(self,request,id):
        branches = Specialization.objects.filter(course = id).values('id','branchName','branchFullname')
        return Response({"branches":branches})


class CourseYearAllowedAPIView(generics.ListCreateAPIView):
    queryset = CourseYearAllowed.objects.all()
    serializer_class = CourseYearAllowedSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = CourseYearAllowedSerializer(data=request.data)
        if serializer.is_valid():
            # print("Valid Data")
            serializer.save()
            return Response({"message":"Company data Inserted successfully"})
        else:
            print(request.data)
            print(serializer.errors)
            return Response(serializer.errors)