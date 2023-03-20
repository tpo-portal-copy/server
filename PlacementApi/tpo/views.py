from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from .models import GeneralAnnouncement, CompanyAnnouncement, Resources
from .serializers import GeneralAnnouncementSerializer,CompanyAnnouncementSerializer, ResourceSerializer
from django.db.models import F, Value, CharField,Q
from django.db.models.functions import Concat


# Create your views here.
class AnnouncementAPIView(generics.ListAPIView):
    serializer_class_General = GeneralAnnouncementSerializer
    serializer_class_Company = CompanyAnnouncementSerializer
    queryset = CompanyAnnouncement.objects.all()

    def get_queryset_General(self):
        return GeneralAnnouncement.objects.all()
    def get_queryset_Company(self):
        return CompanyAnnouncement.objects.all()

    def list(self, request, *args, **kwargs):
        request_type = request.query_params["type"]
        if request_type == "all":
            general = self.serializer_class_General(self.get_queryset_General(), many=True)
            company = self.serializer_class_Company(self.get_queryset_Company(), many=True)
            combined_data = general.data + company.data
            # combined_data = {"general":general,"company":company}
            # sorted_data = CombinedSerializer(combined_data)

            sorted_data = sorted(combined_data, key=lambda x: x['updated_at'], reverse=True)
            print(enumerate(sorted_data))
            temp_data = []
            for i,item in enumerate(sorted_data):
                item["id"] = i
                temp_data.append(item)
            sorted_data = temp_data
            return Response(sorted_data)
        elif ( request_type == "general" or request_type == "results"):
            general = self.serializer_class_General(self.get_queryset_General().filter(type=request_type).order_by("-updated_at"), many=True)
            return Response(general.data)
        elif ( request_type == "company"):
            company = self.serializer_class_Company(self.get_queryset_Company(), many=True)
            return Response(company.data)
        else:
            return Response({"message" : "You got an error while fetching the Announcements List. \n The reason of the Error is Invalid value of announcement type"},status= status.HTTP_400_BAD_REQUEST)

class ResourceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ResourceSerializer
    queryset = Resources.objects.all()
    # filterset_class = ResourcesFilter
    def list(self, request,branch):
        # self.queryset = self.queryset.filter(branch = branch)
        result = {}
        faq = []
        article = []
        if request.query_params.get('term') == None:
            search_term = ""
        else:
            search_term = request.query_params["term"]
        print(search_term)
        self.queryset = self.queryset.filter(Q(branch = branch), Q(heading__icontains = search_term) | Q(content__icontains = search_term))
        for i in self.queryset:
            if i.content_type == "faq":
                faq.append(self.serializer_class(i).data)
            elif i.content_type == "article":
                article.append(self.serializer_class(i).data)
        result["article"] = article
        result["faq"] = faq
        return Response(result)





class ResourceRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ResourceSerializer
    queryset = Resources.objects.all()