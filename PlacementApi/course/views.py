from django.shortcuts import render
from rest_framework import generics, status
from .models import Course, Specialization, CourseYearAllowed
from .serializers import CourseSerializer, SpecialisationSerializer, CourseYearAllowedSerializer
from rest_framework.response import Response

# Create your views here.
class CourseAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SpecializationAPIView(generics.ListCreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecialisationSerializer

class CourseYearAllowedAPIView(generics.ListCreateAPIView):
    queryset = CourseYearAllowed.objects.all()
    serializer_class = CourseYearAllowedSerializer
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