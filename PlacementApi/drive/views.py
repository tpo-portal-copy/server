from django.shortcuts import render
from rest_framework import generics
# from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Drive, Role
from company.models import JNF_intern
from .serializers import DriveSerializer
from student.pagination import CustomPagination
# Create your views here.


class DriveList(generics.ListCreateAPIView):
    # queryset = Drive.objects.select_related('company')
    queryset = Drive.objects.all()
    serializer_class = DriveSerializer
    # filter_backends = (filters.DjangoFilterBackend)
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        for new_role in request.data["other"]:
            Role.objects.get_or_create(name=new_role)
        return super().post(request, *args, **kwargs)

class DriveDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drive.objects.select_related('company')
    serializer_class = DriveSerializer
    