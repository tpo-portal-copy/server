from django.shortcuts import HttpResponse
import pandas as pd
from .models import * 
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from .filters import *
from django_filters import rest_framework as filters
from student.pagination import CustomPagination
# Create your views here.

class ExperienceList(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ExperienceFilter
    pagination_class = CustomPagination

    # def post(self,request):
    #     print(request.data)
    #     se = ExperienceSerializer(data = request.data)
    #     if se.is_valid():
    #         pass
    #     else:
    #         print(se.errors)


class ExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    


        


        

