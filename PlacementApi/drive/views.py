from django.shortcuts import render
from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Drive
from .serializers import DriveSerializer
# Create your views here.


class DriveList(generics.ListCreateAPIView):
    queryset = Drive.objects.select_related('company')
    serializer_class = DriveSerializer
    # filter_backends = (filters.DjangoFilterBackend)

class DriveDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drive.objects.select_related('company')
    serializer_class = DriveSerializer
    