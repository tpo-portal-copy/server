from django.urls import path
from . import views
urlpatterns = [
    path('',views.StudentList.as_view(),name = "list-student"),
    path('countries/',views.CountryListCreateAPIView.as_view(), name="add-countries"),
    path('states/',views.StateListAPIView.as_view(), name="add-states"),
    path('cities/<str:state>',views.CityListAPIView.as_view(), name="add-cities"),
    path('getroutes',views.RouteList.as_view(),name = "get-routes"),
    path('ppo/',views.PPOList.as_view(),name = "ppo-list"),
    path('profile/<str:pk>/',views.StudentDetail.as_view(),name="detail-student"),
    path('detailplacement/',views.StudentPlacementList.as_view(),name=  "list-placement-student"),
    path('detailplacement/<str:pk>',views.StudentPlacementDetail.as_view(),name=  "detail-placement-student"),
    path('detailintern/',views.StudentInternList.as_view(),name=  "list-intern-student"),
    path('detailintern/<str:pk>',views.StudentInternDetail.as_view(),name=  "detail-intern-student"),
    path('detailnotsitting/',views.StudentNotSittingList.as_view(),name=  "list-notsitting-student"),
    path('detailnotsitting/<str:pk>',views.StudentNotSittingDetail.as_view(),name=  "detail-notsitting-student"),
    path('basicstats/',views.BasicStats.as_view(),name = "basic-stats-info"),
    path('companystats/',views.CompanyRelatedQueries.as_view(),name = "basic-stats-info"),
    path('orderwise/',views.CommonQueries.as_view(),name ="stats-by-order"),
    path('placed/',views.StudentPlaced.as_view(),name = "placed-student"),
    path('interned/',views.StudentInterned.as_view(),name = "placed-student"),
    path('recentnotifications/',views.RecentNotifications.as_view(),name = "recent-notification"),
    path('eligibility/<str:roll>',views.EligibilityCheck.as_view(),name = "checker-for-student-eligibility"),
   
    # path('cluster/',clusterchoosen.as_view(),name=  "detail-intern-student"),


]

