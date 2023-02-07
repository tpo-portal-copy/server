from django.shortcuts import render
from .models import Company, HR_details, JNF, JNF_placement, JNF_intern
from .serializers import CompanySerializer, HRSerializer, JNFSerializer, JNFPlacementSerializer, JNFInternSerializer
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
        jnf_list = {"placement":[jnf.jnf.company.name for jnf in JNF_placement.objects.all()],
                    "intern":[jnf.jnf.company.name for jnf in JNF_intern.objects.all()]}
        return Response(jnf_list)

class JNFRetrieveAPIView(generics.RetrieveAPIView):
    queryset = JNF.objects.all()
    serializer_class = JNFSerializer
    lookup_field = ('company__name')
    lookup_url_kwarg = ('company')

class JNFPlacementAPIView(generics.ListAPIView):
    queryset = JNF_placement.objects.all()
    serializer_class = JNFPlacementSerializer

class JNFPlacementRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = JNF_placement.objects.all()
    serializer_class = JNFPlacementSerializer
    lookup_field = ('jnf__company__name')
    lookup_url_kwarg = ('company')

class JNFInternAPIView(generics.ListAPIView):
    queryset = JNF_intern.objects.all()
    serializer_class = JNFInternSerializer

class JNFInternRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = JNF_intern.objects.all()
    serializer_class = JNFInternSerializer
    lookup_field = ('jnf__company__name')
    lookup_url_kwarg = ('company')
