from django.shortcuts import render
from .models import Company, HR_details, JNF
from .serializers import CompanySerializer, HRSerializer, JNFSerializer
# from rest_framework.renderers import JSONRenderer
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

# Create your views here.
# @api_view(['GET','POST'])
# class CompanyAPIView(generics.CreateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer

class CompanyDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = ('name')

class CompanyListAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class HRCreateAPIView(generics.CreateAPIView):
    serializer_class = HRSerializer
    queryset = HR_details.objects.prefetch_related().all()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class HRListAPIView(generics.ListAPIView):
    serializer_class = HRSerializer
    def get_queryset(self):
        company = self.kwargs['name']
        return HR_details.objects.filter(company__name = company)

class HRDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HRSerializer
    queryset = HR_details.objects.all()

class JNFCreateAPIView(generics.CreateAPIView):
    queryset = JNF.objects.all()
    serializer_class = JNFSerializer

class JNFList(APIView):
    def get(self, request):
        jnf_list = {"jnfs":dict([jnf.company.name for jnf in JNF.objects.all()])}
        return Response(jnf_list)
        pass