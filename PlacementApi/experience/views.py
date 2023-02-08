from django.shortcuts import HttpResponse
import pandas as pd
from .models import * 
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from .filters import *
from django_filters import rest_framework as filters
# Create your views here.

# def roll_filling(request):
#     if request.method == 'GET':
#         data = pd.read_csv("roles.txt",header=None,names = ['role'])
#         # print(data)
#         for index, row in data.iterrows():
#             new_role = Role(role = row["role"])
#             new_role.save()
#         return HttpResponse("hii")

class RolesList(APIView):
    # queryset = Role.objects.all()
    # serializer_class = RoleSerializer
    def get(self,request):
        roles = Role.objects.values_list('role',flat = True)
        print(roles)
        roles = {"roles":list(roles)}
        return Response(roles)

class ExperienceList(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ExperienceFilter


class ExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    


        


        

