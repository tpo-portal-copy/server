from django.shortcuts import render,HttpResponse
from .models import Company, HR_details, JNF, JNF_placement, JNF_intern
from .serializers import CompanySerializer, HRSerializer, JNFSerializer, JNFPlacementSerializer, JNFInternSerializer
# from rest_framework.renderers import JSONRenderer
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import generics,filters
from student.pagination import CustomPagination

class CompanyDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = ('name')

class CompanyListAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


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
    def post(self, request, *args, **kwargs):
        # print(request.data)
        jnf = JNFSerializer(data=request.data)

        try:
            Company.objects.get(name = request.data['company'])
        except Company.DoesNotExist:
            serializer = CompanySerializer(data={"name":request.data['company']})
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
                raise APIException("Error in Company Serializer")

        if (not request.data['jnf_intern']) and (not request.data['jnf_placement']):
            print("You cannot insert data with no fields")
            raise APIException("Please provide details from either your internship or placement")

        if(jnf.is_valid()):
            jnf.save()
        else:
            raise APIException(jnf.errors)

        if(request.data['jnf_intern']):
            serializer = JNFInternSerializer(data=request.data['jnf_intern'])
            if(serializer.is_valid()):
                serializer.save()
            else:
                raise APIException(serializer.errors)

        if(request.data['jnf_placement']):
            serializer = JNFPlacementSerializer(data=request.data['jnf_placement'])
            if(serializer.is_valid()):
                serializer.save()
            else:
                raise APIException(serializer.errors)

        if(len(request.data['hr']) > 0):
            for hr in request.data['hr']:
                try:
                    hr_instance = HR_details.objects.get(company__name = hr['company'], type=hr['type'])
                    serializer = HRSerializer(hr_instance, data = {"company":hr['company'], "type":hr['type'],"name":hr["name"],"mobile":hr['mobile'],"email":hr["email"]})
                    if(serializer.is_valid()):
                        serializer.save()
                    else:
                        print(serializer.errors)
                        raise APIException("Error in updating HR_Details due to invalid format")
                except HR_details.DoesNotExist:
                    serializer = HRSerializer(data = {"company":hr['company'], "type":hr['type'],"name":hr["name"],"mobile":hr['mobile'],"email":hr["email"]})
                    if(serializer.is_valid()):
                        serializer.save()
                    else:
                        print(serializer.errors)
                        raise APIException("HR_Details in invalid format")
                except HR_details.MultipleObjectsReturned:
                    raise APIException("Details of multiple HRs present with same type")
        return Response(jnf.data)

class JNFList(APIView):
    def get(self, request):
        jnf_list = {"placement":[jnf.jnf.company.name for jnf in JNF_placement.objects.all()],
                    "intern":[jnf.jnf.company.name for jnf in JNF_intern.objects.all()]}
        return Response(jnf_list)

class JNFRetrieveAPIView(generics.RetrieveUpdateAPIView):
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

class JNFInternCreateAPIView(generics.CreateAPIView):
    queryset = JNF_intern.objects.all()
    serializer_class = JNFInternSerializer

class JNFInternRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = JNF_intern.objects.all()
    serializer_class = JNFInternSerializer
    lookup_field = ('jnf__company__name')
    lookup_url_kwarg = ('company')
