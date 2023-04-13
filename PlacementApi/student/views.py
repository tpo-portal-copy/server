from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import generics
from drive.models import Drive
from .models import *
from .serializers import *
from rest_framework import status
from .filters import StudentPlacementFilter,StudentInternFilter,StudentNSFilter,StudentFilter,PPOFilter
from .pagination import CustomPagination
from django.db.models import Max,Count,Avg,Min
from django.db.models import F
from experience.models import Experience
from rest_framework import permissions
from accounts import permissions as custom_permissions
import pandas as pd

class CountryListCreateAPIView(APIView):
    def post(self,request):
        print(request.data["name"])
        new_country = Country()
        new_country.name = request.data["name"]
        new_country.save()
        return Response(status=status.HTTP_201_CREATED)

class StateListAPIView(APIView):
    def get(self,request):
        state = State.objects.values_list('name',flat=True)
        return Response(state)

    # def post(self,request):
    #     new_state = State(name=request.data["name"], country=Country.objects.get(pk = 101))
    #     new_state.save()
    #     return Response(status=status.HTTP_201_CREATED)

class CityListAPIView(APIView):
    def get(self,request,state):
        city = City.objects.filter(state__name = state).order_by('name').values('id','name')
        return Response(city)

    # def post(self,request):
    #     state,create = State.objects.get_or_create(name = request.data["state"], country=Country.objects.get(pk = 101))
    #     new_city = City(name=request.data["name"], state = state)
    #     new_city.save()
    #     return Response(status=status.HTTP_201_CREATED)


class RouteList(APIView):
    def get(self,request):
        routes = {'student/' : "to get list of students basic info",
                  'student/<str:pk>' : "this will give data of specific student also used for create , update and delete",
                  'student/detailplacement/' : 'to get list of students placement info',
                  'student/detailplacement/<str:pk>' : "this will give data of specific student placement  also used for create , update and delete",
                  'student/detailintern/':"to get list of students placement info",
                  'student/detailintern/<str:pk>':"this will give data of specific student intern also used for create , update and delete",
                  'student/detailnositting/':"to get list of students who are not sitting in placement info",
                  'student/detailintern/<str:pk>':"this will give data of specific student not sitting also used for create , update and delete"}

        return Response(routes)


# API FOR CHECKING ELIGIBILITY OF STUDENT
class EligibilityCheck(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,roll):
        result = {}
        try:
            student = Student.objects.get(roll__username = roll)
            result["eligible"] = CourseYearAllowed.objects.get(course = student.course,year = student.current_year).type_allowed
            print("true")
        except Student.DoesNotExist:
            result["eligible"] = ""
        return Response(result,status=status.HTTP_200_OK)


class PPOList(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = PPO.objects.all() 
    serializer_class = PPOSerializer
    filterset_class = PPOFilter
    pagination_class = CustomPagination
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(),custom_permissions.PlacementSession()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated(),custom_permissions.TPRPermissions()]
        else:
            return []

           

class StudentList(APIView):
    pagination_class = CustomPagination
    filter_class = StudentFilter
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        else:
            return []
    def get(self,request):
        queryset = Student.objects.select_related('roll').all()
        queryset = self.filter_class(request.query_params,queryset).qs
        queryset = queryset.order_by('cgpi')
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        serialized_data = StudentSerializer(queryset,many = True)
        return paginator.get_paginated_response(serialized_data.data)

    def post(self,request): 
        new_student = StudentSerializer(data = request.data)
        print(request.data)
        if new_student.is_valid():
            # print("valid data")
            new_student.save()    
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(request.data)
            print(new_student.errors)
        return Response(new_student.errors,status=status.HTTP_400_BAD_REQUEST)

class StudentDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]  
    def get(self,request,pk):
        students = Student.objects.get(roll__username=pk)
        serialized_data = StudentSerializer(students)
        return Response(serialized_data.data)

    def put(self,request,pk):
        student = Student.objects.get(roll__username = pk)
        update_student = StudentSerializer(instance=student,data = request.data)
        if update_student.is_valid():
            update_student.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(update_student.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        student = Student.objects.get(roll__username = pk)
        print(student)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StudentPlacementList(APIView):
    pagination_class = CustomPagination
    filter_class = StudentPlacementFilter
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        queryset = StudentPlacement.objects.select_related('student').all()
        queryset = queryset.prefetch_related('cluster').all()

        queryset = self.filter_class(request.query_params,queryset).qs
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        serialized_data = StudentPlacementSerializer(queryset,many = True)
        return paginator.get_paginated_response(serialized_data.data)
        # serialized_data = StudentPlacementSerializer(queryset,many = True)
        # return Response(serialized_data.data)

    def post(self,request):
        new_student_placement = StudentPlacementSerializer(data = request.data)
        print(request.data)
        if new_student_placement.is_valid():
            print("valid data")
            new_student_placement.save()   
            return Response(status=status.HTTP_201_CREATED)
        # print(new_student_placement.errors)
        return Response(new_student_placement.errors,status=status.HTTP_400_BAD_REQUEST)

class StudentPlacementDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk):
        # roll = Student.objects.get(roll__username = pk)
        student_placement = StudentPlacement.objects.get(student__roll__username = pk )
        # students = StudentPlacement.objects.get(student = roll)
        serialized_data = StudentPlacementSerializer(student_placement)
        return Response(serialized_data.data)

    def put(self,request,pk):
        student_placement = StudentPlacement.objects.get(student__roll__username = pk)
        update_student_placememt = StudentPlacementSerializer(instance=student_placement,data = request.data)
        if update_student_placememt.is_valid():
            update_student_placememt.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(update_student_placememt.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        student_placement = StudentPlacement.objects.get(student__roll__username = pk)
        student_placement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StudentInternList(APIView):
    filter_class = StudentInternFilter
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        queryset = StudentIntern.objects.select_related('student')
        queryset = self.filter_class(request.query_params,queryset).qs
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        serialized_data = StudentInternSerializer(queryset,many = True)
        return paginator.get_paginated_response(serialized_data.data)
        # serialized_data = StudentInternSerializer(queryset,many = True)
        # return Response(serialized_data.data)

    def post(self,request):
        new_student_intern = StudentInternSerializer(data = request.data)
        if new_student_intern.is_valid():
            new_student_intern.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(new_student_intern.errors,status=status.HTTP_400_BAD_REQUEST)



class StudentInternDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        student_intern = StudentIntern.objects.get(student__roll__username = pk )
        serialized_data = StudentInternSerializer(student_intern)
        return Response(serialized_data.data)

    def put(self,request,pk):
        student_intern= StudentIntern.objects.get(student__roll__username = pk)
        update_student_intern = StudentInternSerializer(instance=student_intern,data = request.data)
        if update_student_intern.is_valid():
            update_student_intern.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(update_student_intern.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        student_intern = StudentIntern.objects.get(student__roll__username = pk)
        student_intern.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentNotSittingList(APIView):
    filter_class = StudentNSFilter
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        queryset = StudentNotSitting.objects.select_related('student')
        queryset = self.filter_class(request.query_params,queryset).qs
        paginator = self.pagination_class()
        queryset = paginator.paginate_queryset(queryset,request)
        serialized_data = StudentInternSerializer(queryset,many = True)
        return paginator.get_paginated_response(serialized_data.data)

    def post(self,request):
        new_student_ns = StudentNotSittingSerializer(data = request.data)
        if new_student_ns.is_valid():
            new_student_ns.save() #owner = request.user    
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(new_student_ns.errors)
        return Response(new_student_ns.errors,status=status.HTTP_400_BAD_REQUEST)



class StudentNotSittingDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,pk):
        student_NS = StudentNotSitting.objects.get(student__roll__username = pk )
        serialized_data = StudentNotSittingSerializer(student_NS)
        return Response(serialized_data.data)

    def put(self,request,pk):
        student_ns= StudentNotSitting.objects.get(student__roll__username = pk)
        update_student_ns = StudentNotSittingSerializer(instance=student_ns,data = request.data)
        if update_student_ns.is_valid():
            update_student_ns.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(update_student_ns.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        student_ns = StudentNotSitting.objects.get(student__roll__username = pk)
        student_ns.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class StudentInterned(generics.ListCreateAPIView):
    queryset = Interned.objects.all()
    serializer_class = InternedSerializer
    permission_classes = [permissions.IsAuthenticated,custom_permissions.TPRPermissions]
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = InternedSerializer(data = request.data)
        if serializer.is_valid():
            # print("Valid Data")
            serializer.save()
            return Response(status= status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentPlaced(generics.ListCreateAPIView):
    queryset = Placed.objects.all()
    serializer_class = PlacedSerializer
    permission_classes = [permissions.IsAuthenticated,custom_permissions.TPRPermissions]
    def post(self, request, *args, **kwargs):
        # print(request.data)
        serializer = PlacedSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status= status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

##################################################################################

# class ClusterChoosen(generics.GenericAPIView):
#     queryset = ClusterChosen.objects.all()
#     serializer_class = ClusterChosenSerializer



class BasicStats(APIView):
    # permission_classes = [permissions.IsAuthenticated]
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
        # print(passingYear)
        print("&&&&&&&&&&&&",session)
        
        statsInfo = []
        result = {}
        
        

        if jtype == "intern":
            topCompaniesIntern = Interned.objects.filter(job_role__drive__session = session).values(name = F('job_role__drive__company__name'),logo =F('job_role__drive__company__logo')).annotate(max_stipend = Max('job_role__ctc')).order_by('-job_role__ctc')[:10]#student__student__passing_year 
            topCompaniesOffCampus = Offcampus.objects.filter(session = session,type = 'intern').values(name = F('company__name'),logo = F('company__logo')).annotate(max_stipend = Max('ctc'))
            topCompanies = topCompaniesIntern.union(topCompaniesOffCampus).order_by('-max_stipend')[:10]
            companiesVisited = Interned.objects.filter(job_role__drive__session = session).values(name = F('job_role__drive__company__name')).distinct().count() 
            print(companiesVisited)
            course_name = request.user.student.course.name
            print(course_name)
            oncampus_data = Interned.objects.filter(job_role__drive__session = session,student__student__course__name = course_name).values(roll = F('student__student'),branch = F('student__student__branch__branch_name'),stipend = F('job_role__ctc'))
            offcampus_data = Offcampus.objects.filter(session = session,type = 'intern',student__course__name = course_name).values(roll=F('student'),branch = F('student__branch__branch_name'),stipend=F('ctc'))
            complete_data = oncampus_data.union(offcampus_data)
            # print(complete_data)
            offers = complete_data.count()
            # print(offers)
            branches = Specialization.objects.filter(course__name = course_name).values_list('branch_name',flat=True)
            complete_data = pd.DataFrame(complete_data)
            temp = 0
            course_wise = []
            # print(complete_data)
    
            for branch in branches:
                total_offers= 0
                max_stipend = 0
                min_stipend = 0
                avg_stipend = 0
                if len(complete_data) == 0:
                    continue
                branch_data = complete_data[complete_data["branch"] == branch]
                if len(branch_data) == 0:
                    branch_wise = {"course":course_name,"branch":branch,"offers":total_offers,"avg_stipend":avg_stipend,"max_stipend":max_stipend,"min_stipend":min_stipend}
                    course_wise.append(branch_wise)
                    continue

                branch_data = branch_data.groupby(['roll']).agg({'stipend' : ['max','mean','sum','min'],'roll':['count','unique']})
                # print(branch_data)
            
                total_student = len(branch_data)
                total_offers = branch_data.get('roll')["count"].sum()
                max_stipend = branch_data.get('stipend')["max"].max()
                min_stipend = branch_data.get('stipend')["max"].min()
                avg_stipend = round(branch_data.get('stipend')["max"].sum()/total_student,2)
                temp += total_offers

                # check = branch_data.get('stipend')["sum"].sum()/total_offers
                # print(max_stipend,min_stipend,avg_stipend,total_offers,check)
                branch_wise = {"course":course_name,"branch":branch,"offers":total_offers,"avg_stipend":avg_stipend,"max_stipend":max_stipend,"min_stipend":min_stipend}
                course_wise.append(branch_wise)
            print(temp)

            totalAppeared = StudentIntern.objects.filter(student__passing_year = passingYear+1).count() # we have to think for mtech and msc 
            course = Course.objects.count()
            serializer = []
            for company in topCompanies:
                serializer.append(company)
            value = [totalAppeared,offers,companiesVisited,course]
            label = ["Student Appeared","Offers","Companies Visited","Courses"]

            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
            result["topCompanies"] = serializer
            result["basicStats"] = course_wise

        elif jtype == "placement":
            topCompaniesPlacement = Placed.objects.filter(job_role__drive__session = session).values(name = F('job_role__drive__company__name'),logo = F('job_role__drive__company__logo')).annotate(max_ctc = Max('job_role__ctc'))
            topCompaniesOffCampus = Offcampus.objects.filter(session = session,type = 'placement').values(name = F('company__name'),logo = F('company__logo')).annotate(max_ctc = Max('ctc'))
            topCompaniesPPO = PPO.objects.filter(session = session).values(name = F('company__name'),logo = F('company__logo')).annotate(max_ctc = Max('ctc'))
            topCompanies = topCompaniesPlacement.union(topCompaniesOffCampus,topCompaniesPPO).order_by('-max_ctc')[:10]
            companiesVisited =  Placed.objects.filter(job_role__drive__session = session).values(name = F('job_role__drive__company__name')).distinct().count()
            course_name = request.user.student.course.name
            oncampus_data = Placed.objects.filter(job_role__drive__session = session,student__student__course__name = course_name).values(roll =F('student__student'),branch = F('student__student__branch__branch_name'),ctc_ = F('job_role__ctc'))
            offcampus_data = Offcampus.objects.filter(session = session,type = 'placement',student__course__name = course_name).values(roll=F('student'),branch = F('student__branch__branch_name'),ctc_=F('ctc'))
            ppo_data = PPO.objects.filter(session = session,student__course__name = course_name).values(roll=F('student'),branch = F('student__branch__branch_name'),ctc_=F('ctc'))
           
            complete_data = oncampus_data.union(offcampus_data,ppo_data) 
            offers = complete_data.count()
            print(offers)
            
            branches = Specialization.objects.filter(course__name = course_name).values_list('branch_name',flat=True)
            complete_data = pd.DataFrame(complete_data)
            temp = 0
            course_wise = []
    
            for branch in branches:
                total_offers= 0
                max_ctc = 0
                min_ctc = 0
                avg_ctc = 0
                branch_data = complete_data[complete_data["branch"] == branch]
                if len(branch_data) == 0:
                    branch_wise = {"course":course_name,"branch":branch,"offers":total_offers,"avg_ctc":avg_ctc,"max_ctc":max_ctc,"min_ctc":min_ctc}
                    course_wise.append(branch_wise)
                    continue

                branch_data = branch_data.groupby(['roll']).agg({'ctc_' : ['max'],'roll':['count']})
            
                total_student = len(branch_data)
                total_offers = branch_data.get('roll')["count"].sum()
                max_ctc = branch_data.get('ctc_')["max"].max()
                min_ctc = branch_data.get('ctc_')["max"].min()
                avg_ctc = round(branch_data.get('ctc_')["max"].sum()/total_student,2)
                temp += total_offers

                   
                branch_wise = {"course":course_name,"branch":branch,"offers":total_offers,"avg_ctc":avg_ctc,"max_ctc":max_ctc,"min_ctc":min_ctc}
                course_wise.append(branch_wise)
            # print(temp)
            totalAppeared = StudentPlacement.objects.filter(student__passing_year = passingYear).count() # we have to think for mtech and msc 
            course = Course.objects.count()
            serializer = []
            for company in topCompanies:
                serializer.append(company)
            value = [totalAppeared,offers,companiesVisited,course]
            label = ["Student Appeared","Offers","Companies Visited","Courses"]

            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
            result["topCompanies"] = serializer
            print(course_wise)
            result["basicStats"] = course_wise
            print(result["basicStats"])

        else:
            studentReceivedPPO = PPO.objects.filter(student__passing_year = passingYear).values('student').distinct().count()
            companiesVisited = PPO.objects.filter(student__passing_year = passingYear).values('company').distinct().count() 
            offers = PPO.objects.filter(student__passing_year = passingYear).count()
            course = Course.objects.all().count()
            value = [studentReceivedPPO,offers,companiesVisited,course]
            label = ["Student Appeared","Offers","Companies Visited","Courses"]

            for i in range(len(label)):
                statsInfo.append({"id":i,"label":label[i],"value" :value[i]})
            result["statsInfo"] = statsInfo
        return Response(result)


class CommonQueries(APIView):
    pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated]


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
        if request.query_params.get('company') == None:
            name = ""
            # raise APIException("Company name can't be empty")
        else:
            name = request.query_params["company"]
        if request.query_params.get('order') == None:
            order = "ctc"
            # raise APIException("Company name can't be empty")
        else:
            order = request.query_params["order"]

        if order == "ctc":
            if jtype == "intern":
                queryset = Interned.objects.filter(job_role__drive__session = session,job_role__drive__company__name__icontains = name).values(name = F('job_role__drive__company__name')).annotate(max_stipend = Max('job_role__ctc')).order_by('-max_stipend')
                print(queryset)
            elif jtype == "placement":
                queryset = Placed.objects.filter(job_role__drive__session = session,job_role__drive__company__name__icontains = name).values(name = F('job_role__drive__company__name')).annotate(max_ctc = Max('job_role__ctc')).order_by('-max_ctc')
            else:
                queryset = PPO.objects.filter(session = session,company__name__icontains = name).values(name = F('company__name')).annotate(max_ctc = Max('ctc')).order_by('-max_ctc')
            paginator = self.pagination_class()
            queryset = paginator.paginate_queryset(queryset,request)
            return paginator.get_paginated_response(queryset) 

        else:
            if jtype == "intern":
                queryset = Interned.objects.filter(job_role__drive__session= session,job_role__drive__company__name__icontains = name).values(name = F('job_role__drive__company__name')).annotate(offers = Count('student')).order_by('-offers')
            elif jtype == "placement":
                queryset = Placed.objects.filter(job_role__drive__session = session,job_role__drive__company__name__icontains = name).values(name = F('job_role__drive__company__name')).annotate(offers = Count('student')).order_by('-offers')
            else:
                queryset = PPO.objects.filter(session = session,company__name__icontains = name).values(name = F('company__name')).annotate(offers = Count('student')).order_by('-offers')               
            paginator = self.pagination_class()
            queryset = paginator.paginate_queryset(queryset,request)
            return paginator.get_paginated_response(queryset) 
        


###################### Statistics Inner Page
class CompanyRelatedQueries(APIView):
    pagination_class = CustomPagination
    # permission_classes = [permissions.IsAuthenticated]

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
        if request.query_params.get('company') == None:
            raise APIException("Company name can't be empty")
        else:
            company = request.query_params["company"]
        
        # print(jtype)
        # print(session)
        # print(company)
        result = {}
        result['company']=company
        result['totalOffers']=0
        result['courses']=[]

        # courses_list = [ course.name for course in Course.objects.all() ]
        courses_list = Course.objects.values_list('name', flat=True)
        print(courses_list)


        queryset = None
        if jtype == "intern":
            Main_Model = Interned

        elif jtype == "placement":
            Main_Model = Placed

        queryset_1 = Main_Model.objects.filter(job_role__drive__session = session,job_role__drive__company__name__iexact = company)
        queryset_1 = queryset_1.values(course = F('student__student__course__name'), branch = F('student__student__branch__branch_name'), role = F('job_role__role__name'), curr_ctc = F('job_role__ctc')).annotate(offers=Count('student'))
        # print(queryset_1)

        queryset_2 = Offcampus.objects.filter(session = session, company__name = company, type = jtype)
        queryset_2 = queryset_2.values(course = F('student__course__name'), branch = F('student__branch__branch_name'), role = F('profile__name'), curr_ctc = F('ctc')).annotate(offers=Count('student'))
        # print(queryset_2)

        queryset = list(queryset_1.union(queryset_2, all=True))
        # queryset = queryset_1 | queryset_2
        print(queryset)
        print(type(queryset))

        # return Response(status=status.HTTP_202_ACCEPTED)

        for i,course in enumerate(courses_list):
            # print(course)
            # course_queryset = queryset_1.filter(course = course).union(queryset_2.filter(course = course))
            # print("Course Queryset = ",course_queryset)
            curr_course_result = {}

            curr_course_result['id'] = i
            curr_course_result['courseName'] = course
            curr_course_result['totalCourseOffers']=0


            curr_course_result['roles'] = []
            # roles_list = queryset_1.values_list('role','curr_ctc','job_role__role__name').distinct()
            roles_list = list(set([(x['role'],x['curr_ctc']) for x in queryset]))
            print(roles_list)

            for j,role in enumerate(roles_list):
                curr_role_result = {}
                curr_role_result['id'] = j
                curr_role_result['roleName'] = role[0]
                curr_role_result['ctc'] = role[1]
                # curr_role_result['JobRoleID'] = role[2]
                curr_course_result['roles'].append(curr_role_result)
            print(curr_course_result['roles'])
            # return Response(status=status.HTTP_202_ACCEPTED)


            curr_course_result['branches'] = []
            branches_list = Specialization.objects.filter(course__name = course).values_list('branch_name',flat=True)
            # print(branches_list)

            for j,branch in enumerate(branches_list):
                # branch_queryset = course_queryset.filter(student__student__branch__branch_name = branch)
                # print(course,":",branch)
                # print(branch_queryset)
                # return Response(status=status.HTTP_202_ACCEPTED)
                curr_branch_result = {}
                curr_branch_result['id'] = j
                curr_branch_result['branchName'] = branch
                curr_branch_result['totalBranchOffers'] = 0
                curr_branch_result['offersRoleWise'] = []

                for k,role_data in enumerate(curr_course_result['roles']):
                    # print(role_data)
                    # final_queryset = branch_queryset.filter(job_role=role_data['JobRoleID']).values(role = F('job_role')).annotate(offers = Count('student')).order_by('-offers')
                    # final_queryset = queryset_1.filter(course=course, branch=branch, )
                    final_queryset = list(filter(lambda x: x["course"] == course and x["branch"] == branch and x["role"] == role_data['roleName'] and x["curr_ctc"] == role_data["ctc"], queryset))

                    # print(k,role_data)
                    # print(final_queryset)
                    # return Response(status=status.HTTP_202_ACCEPTED)

                    curr_branch_role_result = {}
                    curr_branch_role_result['id'] = k
                    if final_queryset:
                        curr_branch_role_result['noOfOffers'] = final_queryset[0]["offers"]
                    else:
                        curr_branch_role_result['noOfOffers'] = 0

                    curr_branch_result['totalBranchOffers'] += curr_branch_role_result["noOfOffers"]

                    curr_branch_result['offersRoleWise'].append(curr_branch_role_result)
                # print(curr_branch_result)
                curr_course_result['branches'].append(curr_branch_result)

                curr_course_result['totalCourseOffers'] += curr_branch_result['totalBranchOffers']
            result['courses'].append(curr_course_result)

            result['totalOffers'] += curr_course_result['totalCourseOffers']
   
        return Response(result)

      

    


 ########################## Dashboard API 
class RecentNotifications(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        result = {}
        recentDrive = Drive.objects.all().order_by('-starting_date')[:5]
        recentExperience = Experience.objects.all().order_by('-created_at')[:5]
        print(recentDrive)
        serializerdrive = []
        for drive in recentDrive:
           serializerdrive.append({'Id' : drive.id,'Company':drive.company.name,'Starting_Date':drive.starting_date,'Image_Url':"https://picsum.photos/100"})
        result["Recent_Drive"] = serializerdrive

        serializerexperience = []
        for exp in recentExperience:
            serializerexperience.append({'Id' : exp.id,'Name':exp.student.first_name,'Created_Date':exp.created_at.date(),'Image_Url':"https://picsum.photos/100"})
        result["Recent_Experience"] = serializerexperience
        return Response(result)