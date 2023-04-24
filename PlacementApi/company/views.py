from django.shortcuts import render
from .models import Company, HR_details, JNF, JNF_placement, JNF_intern, JNF_intern_fte
from .serializers import CompanySerializer, HRSerializer, JNFSerializer, JNFPlacementSerializer, JNFInternSerializer, JNFInternFTESerializer, JNF_TPO_Serializer
from accounts.utils import GetSession
# from rest_framework.renderers import JSONRenderer
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import generics,filters
from rest_framework import permissions
from accounts import permissions as custom_permissions
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

        if ((not 'jnfIntern' in request.data) and (not 'jnfPlacement' in request.data) and (not 'jnf_six_months_intern' in request.data)):
            print("Provide details from either your internship or placement or internship FTE")
            raise APIException("Please provide details from either your internship or placement or internship FTE")

        if((not 'hr_details' in request.data) or len(request.data['hr_details']) == 0):
            raise APIException('Data cannot be inserted without HR Details')

        if(jnf.is_valid()):
            jnf.save()
        else:
            raise APIException(jnf.errors)

        if(('jnfIntern' in request.data) and request.data['jnfIntern']):
            for dat in request.data['jnfIntern']:
                jnf_intern_data = dat
                jnf_intern_data['jnf'] = request.data['company']
                serializer = JNFInternSerializer(data=jnf_intern_data)
                if(serializer.is_valid()):
                    serializer.save()
                else:
                    raise APIException(serializer.errors)

        if(('jnfPlacement' in request.data) and request.data['jnfPlacement']):
            for dat in request.data['jnfPlacement']:
                jnf_placement_data = dat
                jnf_placement_data['jnf'] = request.data['company']
                serializer = JNFPlacementSerializer(data=jnf_placement_data)
                if(serializer.is_valid()):
                    serializer.save()
                else:
                    raise APIException(serializer.errors)

        if(('jnf_six_months_intern' in request.data) and request.data['jnf_six_months_intern']):
            for dat in request.data['jnf_six_months_intern']:
                jnf_six_months_intern_data = dat
                jnf_six_months_intern_data['jnf'] = request.data['company']
                serializer = JNFInternFTESerializer(data=jnf_six_months_intern_data)
                if(serializer.is_valid()):
                    serializer.save()
                else:
                    raise APIException(serializer.errors)

        if(len(request.data['hr_details']) > 0):
            for hr in request.data['hr_details']:
                try:
                    hr_instance = HR_details.objects.get(company__name = request.data['company'], type=hr['type'])
                    serializer = HRSerializer(hr_instance, data = {"company":request.data['company'], "type":hr['type'],"name":hr["name"],"mobile":hr['mobile'],"email":hr["email"]})
                    if(serializer.is_valid()):
                        serializer.save()
                    else:
                        print(serializer.errors)
                        raise APIException("Error in updating HR_Details due to invalid format")
                except HR_details.DoesNotExist:
                    serializer = HRSerializer(data = {"company":request.data['company'], "type":hr['type'],"name":hr["name"],"mobile":hr['mobile'],"email":hr["email"]})
                    if(serializer.is_valid()):
                        serializer.save()
                    else:
                        print(serializer.errors)
                        raise APIException("HR_Details in invalid format")
                except HR_details.MultipleObjectsReturned:
                    raise APIException("Details of multiple HRs present with same type")
        return Response(jnf.data)

class JNFList(generics.ListAPIView):
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'LIST':
            return [permissions.IsAuthenticated(), custom_permissions.TPO_TPR_Permissions()]

    # queryset = JNF.objects.filter(session=GetSession().CurrentSession())
    serializer_class = JNF_TPO_Serializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated and self.request.user.is_staff:
            return JNF.objects.filter(session=GetSession().CurrentSession())
        else:
            return JNF.approved.filter(session=GetSession().CurrentSession())

class JNFRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = JNF.objects.all()
    serializer_class = JNFSerializer

class JNFRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    # queryset = JNF.objects.all()
    serializer_class = JNFSerializer
    lookup_field = ('company__name')
    lookup_url_kwarg = ('company')

    def get_queryset(self):
        session = self.kwargs['session']
        queryset = JNF.objects.filter(session=session)
        return queryset

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
