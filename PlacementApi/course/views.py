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
    
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class SpecializationAPIView(generics.ListCreateAPIView):

    queryset = Specialization.objects.all()
    serializer_class = SpecialisationSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class SpecilizationDetailAPIView(views.APIView):
  
    def get(self,request,id):
        branches = Specialization.objects.filter(course = id).values('id','branch_name')
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