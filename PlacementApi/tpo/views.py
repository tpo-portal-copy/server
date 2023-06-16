from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import APIException

from student.pagination import CustomPagination
from .models import GeneralAnnouncement, CompanyAnnouncement, Resources
from .serializers import GeneralAnnouncementSerializer,CompanyAnnouncementSerializer, ResourceSerializer
from django.db.models import F,Q,Max,Avg
from accounts import permissions as custom_permissions
from django.utils import timezone
from student.models import Placed,Interned,Offcampus,PPO,StudentPlacement,StudentIntern
from course.models import Course,Specialization
import pandas as pd
from .filters import CompanyWiseFilter
# Create your views here.
class AnnouncementAPIView(generics.ListCreateAPIView):
    serializer_class_General = GeneralAnnouncementSerializer
    serializer_class_Company = CompanyAnnouncementSerializer
    queryset = CompanyAnnouncement.objects.all()
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'POST':
            return [custom_permissions.TPOPermissions()] # custom_permissions.TPRPermissions()]
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
        elif request_type == "placement/intern":
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
            [custom_permissions.TPRPermissions()] # custom_permissions.TPOPermissions()]
        else:
            return []
    def list(self, request,branch):
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

        months = [(7,'July'),(8,'Aug'),(9,'Sep'),(10,'Oct'),(11,'Nov'),(12,'Dec'),(1,'Jan'),(2,'Feb'),(3,'March'),(4,'April'),(5,'May'),(6,'June')]
        courseMonthWise = {}
        for m in months:
            courseMonthWise[m[0]] = {'month' : m[1]}
        # return 
    
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
            for i,course in enumerate(courses):
                total_offers= 0
                max_stipend = 0
                min_stipend = 0
                avg_stipend = 0
                total_student = 0
                courseData = df[df["course"] == course]

                ######### stacked bar chart info 
                monthWise = courseData.groupby(['month'])["roll"].count()
                for key in monthWise.index:
                    courseMonthWise[key][course] = monthWise[key]     
                
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
            averageIn = 0
            if totalStudentPlaced:
                averageIn = round(totalSum/totalStudentPlaced,2)
            value = [totalAppeared,totalStudentPlaced,offers,companiesVisited,course,averageIn]
            label = ["Student Appeared","Selections","Offers","Companies Visited","Courses","Average Stipend"]
            statsInfo = []
            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
            result["topCompanies"] = serializer
            result["basicStats"] = courseWise   
            result["monthWise"] = list(courseMonthWise.values())

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
            for i,course in enumerate(courses):
                total_offers= 0
                max_ctc = 0
                min_ctc = 0
                avg_ctc = 0
                total_student = 0
                courseData = df[df["course"] == course]
                ######### stacked bar chart 
                monthWise = courseData.groupby(['month'])["roll"].count()
                
                for key in monthWise.index:
                    courseMonthWise[key][course] = monthWise[key]     
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
            averagePl = 0
            if totalStudentPlaced:
                averagePl = round(totalSum/totalStudentPlaced,2)
            value = [totalAppeared,totalStudentPlaced,offers,companiesVisited,course,averagePl]
            label = ["Student Appeared","Selections","Offers","Companies Visited","Courses","Average CTC"]
            statsInfo = []
            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
            result["topCompanies"] = serializer
            result["basicStats"] = courseWise
            result["monthWise"] = list(courseMonthWise.values())
        else:
            totalAppeared = PPO.objects.filter(session = session).values('student').count()
            studentReceivedPPO = PPO.objects.filter(session = session).values('student').distinct().count()
            companiesVisited = PPO.objects.filter(session = session).values('company').distinct().count() 
            offers = PPO.objects.filter(session = session).count()
            course = Course.objects.all().count()
            averagePPO = PPO.objects.filter(session = session).values('student').annotate(max_ctc = Max('ctc'))
            averagePPO =averagePPO.aggregate(Avg('max_ctc'))
            value = [totalAppeared,studentReceivedPPO,offers,companiesVisited,course,averagePPO['max_ctc__avg']]
            label = ["Student Appeared","Total student recieved PPO","Offers","Companies Visited","Courses","Average CTC"]
            statsInfo = []
            result = {}
            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
            result["monthWise"] = []


        return Response(result,status=status.HTTP_200_OK)

####### company wise stats
class CompanyWiseStats(APIView):
    pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated]
    filter_class = CompanyWiseFilter

    def get(self, request, *args, **kwargs):

        if request.query_params.get('session') == None:
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
        if request.query_params.get('company') == None:
            raise APIException("Company name can't be empty")
        else:
            company = request.query_params["company"]

        result = {}
        result["company"] = company
        print(jtype)

        if jtype == "intern":
            oncampusData = Interned.objects.filter(job_role__drive__session = session,job_role__drive__company__name = company).values(fname = F('student__student__first_name'),mname = F('student__student__middle_name'),lname = F('student__student__last_name'),rollNumber = F('student__student__roll__username'),branch = F('student__student__branch__branchName'),course = F('student__student__course__name'),ctc_offered = F('job_role__ctc'),clusterc = F('job_role__cluster'),jobRole = F("job_role__role__name"))
            offcampusData = Offcampus.objects.filter(session = session,type=jtype,company__name = company).values(fname = F('student__first_name'),mname = F('student__middle_name'),lname = F('student__last_name'),rollNumber = F('student__roll__username'),branch = F('student__branch__branchName'),course = F('student__course__name'),ctc_offered = F('ctc'),clusterc = F('cluster'),jobRole = F("profile__name")) # change branchName to branchFullname
            oncampusData = self.filter_class(request.query_params,oncampusData).qs
            offcampusData = self.filter_class(request.query_params,offcampusData).qs
            completeData = oncampusData.union(offcampusData)
            result['totaloffers'] = completeData.count()

        else:
            oncampusData = Placed.objects.filter(job_role__drive__session = session,job_role__drive__company__name = company).values(fname = F('student__student__first_name'),mname = F('student__student__middle_name'),lname = F('student__student__last_name'),rollNumber = F('student__student__roll__username'),branch = F('student__student__branch__branchName'),course = F('student__student__course__name'),ctc_offered = F('job_role__ctc'),clusterc = F('job_role__cluster'),jobRole = F("job_role__role__name"))
            offcampusData = Offcampus.objects.filter(session = session,type=jtype,company__name = company).values(fname = F('student__first_name'),mname = F('student__middle_name'),lname = F('student__last_name'),rollNumber = F('student__roll__username'),branch = F('student__branch__branchName'),course = F('student__course__name'),ctc_offered = F('ctc'),clusterc = F('cluster'),jobRole = F("profile__name"))
            ppoData = PPO.objects.filter(session = session,company__name = company).values(fname = F('student__first_name'),mname = F('student__middle_name'),lname = F('student__last_name'),rollNumber = F('student__roll__username'),branch = F('student__branch__branchName'),course = F('student__course__name'),ctc_offered = F('ctc'),clusterc = F('cluster'),jobRole = F("profile__name")) ## change branchName to branchFullname
            oncampusData = self.filter_class(request.query_params,oncampusData).qs
            offcampusData = self.filter_class(request.query_params,offcampusData).qs
            ppoData = self.filter_class(request.query_params,ppoData).qs
            completeData = oncampusData.union(offcampusData,ppoData)
            
            result['totaloffers'] = completeData.count()
        selectedStudents = []
        for i,val in enumerate(completeData):
            name = val.pop('fname')
            lname = val.pop('lname')
            mname = val.pop('mname')
            if lname:
                name += " " + lname
            if mname:
                name += " " + mname
            val["name"] = name
            selectedStudents.append({'id' : i,**val})
        result["selectedStudents"] = selectedStudents
        return Response(result)


##################### placed student data   
class StudentWiseStats(APIView):
    pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated]
    filter_class = CompanyWiseFilter

    def get(self, request, *args, **kwargs):

        if request.query_params.get('session') == None:
            curr_date = timezone.now()
            date = timezone.datetime(curr_date.year, 7, 1, tzinfo=timezone.get_current_timezone())
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            if curr_date <= date:
                session = str(curr_date.year-1) + "-"+str(curr_date.year)[2:]
            else:
                session = str(curr_date.year) + "-"+str(curr_date.year+1)[2:]
        else:
            session = request.query_params["session"]
        if request.query_params.get('jtype') == None:
            jtype = "placement"
        else:
            jtype = request.query_params["jtype"]

        if request.query_params.get("course") == None or request.query_params.get("course") == "":
            course = "B.Tech"
        else:
            course = request.query_params["course"]


        result = {}
        print(session,jtype,course)
        if jtype == "intern":
            oncampusData = Interned.objects.filter(job_role__drive__session = session).values(fname = F('student__student__first_name'),mname = F('student__student__middle_name'),lname = F('student__student__last_name'),rollNumber = F('student__student__roll__username'),branch = F('student__student__branch__branchFullname'),course = F('student__student__course__name'),ctc_offered = F('job_role__ctc'),clusterc = F('job_role__cluster'),companyName = F('job_role__drive__company__name'))
            offcampusData = Offcampus.objects.filter(session = session,type=jtype).values(fname = F('student__first_name'),mname = F('student__middle_name'),lname = F('student__last_name'),rollNumber = F('student__roll__username'),branch = F('student__branch__branchFullname'),course = F('student__course__name'),ctc_offered = F('ctc'),clusterc = F('cluster'),companyName = F('company__name'))
            oncampusData = self.filter_class(request.query_params,oncampusData).qs
            offcampusData = self.filter_class(request.query_params,offcampusData).qs
            completeData = oncampusData.union(offcampusData)
            var = "stipend"
       

        else:
            oncampusData = Placed.objects.filter(job_role__drive__session = session).values(fname = F('student__student__first_name'),mname = F('student__student__middle_name'),lname = F('student__student__last_name'),rollNumber = F('student__student__roll__username'),branch = F('student__student__branch__branchFullname'),course = F('student__student__course__name'),ctc_offered = F('job_role__ctc'),clusterc = F('job_role__cluster'),companyName = F("job_role__drive__company__name"))
            offcampusData = Offcampus.objects.filter(session = session,type=jtype).values(fname = F('student__first_name'),mname = F('student__middle_name'),lname = F('student__last_name'),rollNumber = F('student__roll__username'),branch = F('student__branch__branchFullname'),course = F('student__course__name'),ctc_offered = F('ctc'),clusterc = F('cluster'),companyName = F('company__name'))
            ppoData = PPO.objects.filter(session = session).values(fname = F('student__first_name'),mname = F('student__middle_name'),lname = F('student__last_name'),rollNumber = F('student__roll__username'),branch = F('student__branch__branchFullname'),course = F('student__course__name'),ctc_offered = F('ctc'),clusterc = F('cluster'),companyName = F("company__name"))
            oncampusData = self.filter_class(request.query_params,oncampusData).qs
            offcampusData = self.filter_class(request.query_params,offcampusData).qs
            ppoData = self.filter_class(request.query_params,ppoData).qs
            completeData = oncampusData.union(offcampusData,ppoData)
            var = 'ctc'
            # print(completeData)
        result["totalOffers"] = completeData.count()            
        selectedStudents = []
        for i,val in enumerate(completeData):
            name = val.pop('fname')
            lname = val.pop('lname')
            mname = val.pop('mname')
            if lname:
                name += " " + lname
            if mname:
                name += " " + mname
            val["name"] = name
            selectedStudents.append({'id' : i,**val})

        result["selectedStudents"] = selectedStudents

        branches = Specialization.objects.filter(course__name = course).values_list('branchFullname',flat=True)
        complete_data = pd.DataFrame(completeData)
        course_wise = []
        complete_data = complete_data[complete_data["course"] == course]
        for branch in branches:
            total_offers= 0
            max_stipend = 0
            min_stipend = 0
            avg_stipend = 0
            if len(complete_data) == 0:
                continue
            branch_data = complete_data[complete_data["branch"] == branch]
            if len(branch_data) == 0:
                branch_wise = {"course":course,"branch":branch,"offers":total_offers,"avg_{0}".format(var):avg_stipend,"max_{0}".format(var):max_stipend,"min_{0}".format(var):min_stipend}
                course_wise.append(branch_wise)
                continue

            branch_data = branch_data.groupby(['rollNumber']).agg({'ctc_offered' : ['max','mean','sum','min'],'rollNumber':['count']})
            total_student = len(branch_data)
            total_offers = branch_data.get('rollNumber')["count"].sum()
            max_stipend = branch_data.get('ctc_offered')["max"].max()
            min_stipend = branch_data.get('ctc_offered')["max"].min()
            avg_stipend = round(branch_data.get('ctc_offered')["max"].sum()/total_student,2)
            branch_wise = {"course":course,"branch":branch,"offers":total_offers,"avg_{0}".format(var):avg_stipend,"max_{0}".format(var):max_stipend,"min_{0}".format(var):min_stipend}
            course_wise.append(branch_wise)
        result["courseWise"] = course_wise
        return Response(result)


        


        
    




