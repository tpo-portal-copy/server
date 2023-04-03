from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from .models import GeneralAnnouncement, CompanyAnnouncement, Resources
from .serializers import GeneralAnnouncementSerializer,CompanyAnnouncementSerializer, ResourceSerializer
from django.db.models import F, Value, CharField,Q,Max,Avg,Count
from django.db.models.functions import Concat
from accounts import permissions as custom_permissions
from django.utils import timezone
from student.models import Placed,Interned,Offcampus,PPO,StudentPlacement,StudentIntern
from course.models import Course
import pandas as pd

# Create your views here.
class AnnouncementAPIView(generics.ListCreateAPIView):
    serializer_class_General = GeneralAnnouncementSerializer
    serializer_class_Company = CompanyAnnouncementSerializer
    queryset = CompanyAnnouncement.objects.all()
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'POST':
            return [custom_permissions.TPOPermissions()|custom_permissions.TPRPermissions()]
        else:
            return []
   

    def get_queryset_General(self):
        return GeneralAnnouncement.objects.all()
    def get_queryset_Company(self):
        return CompanyAnnouncement.objects.all()

    def post(self, request, *args, **kwargs):
        print(request.data)
        request_type = request.data["type"]
        print(request_type)

        serializer = None
        if request_type == "general" or request_type == "results":
            serializer = self.serializer_class_General(data=request.data)
            pass
        elif request_type == "company":
            serializer = self.serializer_class_Company(data=request.data)
            pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'POST':
            return [custom_permissions.TPOPermissions()|custom_permissions.TPRPermissions()]
        else:
            return []
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
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'PUT':
            return [custom_permissions.TPOPermissions()|custom_permissions.TPRPermissions()]
        else:
            return []
        
    



################################################ Statistics front page 


class CollegePlacementStats(APIView):
    def get(self,request):
        if request.query_params.get('session') == None or request.query_params["session"] == "":
            curr_date = timezone.now()
            date = timezone.datetime(curr_date.year, 7, 1, tzinfo=timezone.get_current_timezone())
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            if curr_date <= date:
                session = str(curr_date.year-1) + "-"+str(curr_date.year)[2:]
            else:
                session = str(curr_date.year) + "-"+str(curr_date.year+1)[2:]
        else:
            session = request.query_params["session"]
        if request.query_params.get('type') == None:
            jtype = "placement"
        else:
            jtype = request.query_params["type"]

        passingYear = "20" + session[5:]
        passingYear = int(passingYear)
        print(passingYear)

        if jtype == "intern":
            topCompaniesIntern = Interned.objects.filter(job_role__drive__session = session).values(name = F('job_role__drive__company__name'),logo =F('job_role__drive__company__logo')).annotate(max_stipend = Max('job_role__ctc')).order_by('-job_role__ctc')[:10]#student__student__passing_year 
            topCompaniesOffCampus = Offcampus.objects.filter(session = session,type = 'intern').values(name = F('company__name'),logo = F('company__logo')).annotate(max_stipend = Max('ctc'))
            topCompanies = topCompaniesIntern.union(topCompaniesOffCampus).order_by('-max_stipend')[:10]
            companiesVisited = Interned.objects.filter(job_role__drive__session = session).values(name = F('job_role__drive__company__name')).distinct().count()
            oncampusData = Interned.objects.filter(job_role__drive__session = session).values(roll = F('student__student__roll__username'),course = F('student__student__course__name'),stipend = F('job_role__ctc'),month = F('created_at__month'),year = F('created_at__year'))
            OffcampusData = Offcampus.objects.filter(session = session,type = 'intern').values(roll = F('student__roll__username'),course = F('student__course__name'),stipend = F('ctc'),month = F('created_at__month'),year = F('created_at__year'))
            completeData = oncampusData.union(OffcampusData)
            offers = completeData.count()
            # print(offers)
            courses = Course.objects.all().values_list('name',flat=True)
            df = pd.DataFrame(completeData) 
            courseWise = []
            totalStudentPlaced = 0
            result = {}
            totalSum = 0   # to calculate the avg of overall stipend
            courseMonthWise = []
            for course in courses:
                total_offers= 0
                max_stipend = 0
                min_stipend = 0
                avg_stipend = 0
                total_student = 0
                courseData = df[df["course"] == course]

                ######### line chart info 
                monthWise = courseData.groupby(['month'])["roll"].count()
                months = {}
                m = [(7,'July'),(8,'Aug'),(9,'Sep'),(10,'Oct'),(11,'Nov'),(12,'Dec'),(1,'Jan'),(2,'Feb'),(3,'March'),(4,'April'),(5,'May'),(6,'June')]
                for index,key in m:
                    months[index] = ({'month':key,"offers":0})
                for key in monthWise.index:
                    months[key][offers] = monthWise[key]
                val = list(months.values())
                courseMonthWise.append({course : val})
                total_offers = len(courseData)
                if total_offers == 0:
                    course_wise = {"course":course,"offers":total_offers,"total_student":total_student,"avg_stipend":avg_stipend,"max_stipend":max_stipend,"min_stipend":min_stipend}
                    courseWise.append(course_wise)
                    continue
                courseDataGroupBy = courseData.groupby(['roll']).agg({'stipend' : ['max','mean','count']}) 
                total_student = len(courseDataGroupBy)
                total_sum = courseDataGroupBy.get('stipend')["max"].sum()
                max_stipend = courseDataGroupBy.get('stipend')["max"].max()
                min_stipend = courseDataGroupBy.get('stipend')["max"].min()
                avg_stipend = round(courseDataGroupBy.get('stipend')["max"].sum()/total_student,2)
                course_wise = {"course":course,"offers":total_offers,"total_student":total_student,"avg_stipend":avg_stipend,"max_stipend":max_stipend,"min_stipend":min_stipend}
                courseWise.append(course_wise)
                totalStudentPlaced += total_student
                totalSum += total_sum
            print(courseWise)
            totalAppeared = StudentIntern.objects.filter(student__passing_year = passingYear+1).count() # we have to think for mtech and msc 
            course = Course.objects.count()
            serializer = []
            for company in topCompanies:
                serializer.append(company)
            value = [totalAppeared,totalStudentPlaced,offers,companiesVisited,course,round(totalSum/totalStudentPlaced,2)]
            label = ["Student Appeared","Total Student Got Intern","Offers","Companies Visited","Courses","Avg"]
            statsInfo = []
            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
            result["topCompanies"] = serializer
            result["basicStats"] = courseWise   
            result["monthWise"] = courseMonthWise

        elif jtype == "placement":
            topCompaniesIntern = Placed.objects.filter(job_role__drive__session = session).values(name = F('job_role__drive__company__name'),logo =F('job_role__drive__company__logo')).annotate(max_ctc = Max('job_role__ctc')).order_by('-max_ctc')[:10]#student__student__passing_year 
            topCompaniesOffCampus = Offcampus.objects.filter(session = session,type = 'placement').values(name = F('company__name'),logo = F('company__logo')).annotate(max_ctc = Max('ctc'))
            topCompaniesPPO = PPO.objects.filter(session = session).values(name = F('company__name'),logo = F('company__logo')).annotate(max_ctc = Max('ctc'))
            topCompanies = topCompaniesIntern.union(topCompaniesOffCampus,topCompaniesPPO).order_by('-max_ctc')[:10]
            companiesVisited = Placed.objects.filter(job_role__drive__session = session).values(name = F('job_role__drive__company__name')).distinct().count()
            oncampusData = Placed.objects.filter(job_role__drive__session = session).values(roll = F('student__student__roll__username'),course = F('student__student__course__name'),ctc_ = F('job_role__ctc'),month = F('created_at__month'),year = F('created_at__year'))
            OffcampusData = Offcampus.objects.filter(session = session,type = 'placement').values(roll = F('student__roll__username'),course = F('student__course__name'),ctc_ = F('ctc'),month = F('created_at__month'),year = F('created_at__year'))
            ppoData = PPO.objects.filter(session = session).values(roll = F('student__roll__username'),course = F('student__course__name'),ctc_ = F('ctc'),month = F('created_at__month'),year = F('created_at__year'))
            completeData = oncampusData.union(OffcampusData,ppoData)
            offers = completeData.count()   
            courses = Course.objects.all().values_list('name',flat=True)
            df = pd.DataFrame(completeData) 
            courseWise = []
            totalStudentPlaced = 0
            result = {}
            totalSum = 0   # to calculate the avg of overall stipend
            courseMonthWise = []

            for course in courses:
                total_offers= 0
                max_ctc = 0
                min_ctc = 0
                avg_ctc = 0
                total_student = 0
                courseData = df[df["course"] == course]
                ######### line chart info 
                monthWise = courseData.groupby(['month'])["roll"].count()
                months = {}
                m = [(7,'July'),(8,'Aug'),(9,'Sep'),(10,'Oct'),(11,'Nov'),(12,'Dec'),(1,'Jan'),(2,'Feb'),(3,'March'),(4,'April'),(5,'May'),(6,'June')]
                for index,key in m:
                    months[index] = ({'month':key,"offers":0})
                for key in monthWise.index:
                    months[key][offers] = monthWise[key]
                val = list(months.values())
                courseMonthWise.append({course : val})
                total_offers = len(courseData)
                if total_offers == 0:
                    course_wise = {"course":course,"offers":total_offers,"total_student":total_student,"avg_ctc":avg_ctc,"max_ctc":max_ctc,"min_ctc":min_ctc}
                    courseWise.append(course_wise)
                    continue
                courseDataGroupBy = courseData.groupby(['roll']).agg({'ctc_' : ['max','mean','count']}) 
                total_student = len(courseDataGroupBy)
                total_sum = courseDataGroupBy.get('ctc_')["max"].sum()
                max_ctc = courseDataGroupBy.get('ctc_')["max"].max()
                min_ctc = courseDataGroupBy.get('ctc_')["max"].min()
                avg_ctc = round(courseDataGroupBy.get('ctc_')["max"].sum()/total_student,2)
                course_wise = {"course":course,"offers":total_offers,"total_student":total_student,"avg_ctc":avg_ctc,"max_ctc":max_ctc,"min_ctc":min_ctc}
                courseWise.append(course_wise)
                totalStudentPlaced += total_student
                totalSum += total_sum
            print(courseWise)
            totalAppeared = StudentPlacement.objects.filter(student__passing_year = passingYear).count() # we have to think for mtech and msc 
            course = Course.objects.count()
            serializer = []
            for company in topCompanies:
                serializer.append(company)
            value = [totalAppeared,totalStudentPlaced,offers,companiesVisited,course,round(totalSum/totalStudentPlaced,2)]
            label = ["Student Appeared","Total Student Got Placement","Offers","Companies Visited","Courses","Avg"]
            statsInfo = []
            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
            result["topCompanies"] = serializer
            result["basicStats"] = courseWise
            result["monthWise"] = courseMonthWise
        else:
            totalAppeared = PPO.objects.filter(student__passing_year = passingYear).values('student').count()
            studentReceivedPPO = PPO.objects.filter(student__passing_year = passingYear).values('student').distinct().count()
            companiesVisited = PPO.objects.filter(student__passing_year = passingYear).values('company').distinct().count() 
            offers = PPO.objects.filter(student__passing_year = passingYear).count()
            course = Course.objects.all().count()
            value = [totalAppeared,studentReceivedPPO,offers,companiesVisited,course]
            label = ["Student Appeared","Total student recieved PPO","Offers","Companies Visited","Courses"]
            statsInfo = []
            result = {}
            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo

        return Response(result,status=status.HTTP_200_OK)




        


        
    




