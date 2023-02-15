from django.urls import path
from .views import *
urlpatterns = [
    path('',StudentList.as_view(),name = "list-student"),
    path('getroutes',RouteList.as_view(),name = "get-routes"),
    path('ppo/',PPOList.as_view(),name = "ppo-list"),
    path('<str:pk>',StudentDetail.as_view(),name="detail-student"),
    path('detailplacement/',StudentPlacementList.as_view(),name=  "list-placement-student"),
    path('detailplacement/<str:pk>',StudentPlacementDetail.as_view(),name=  "detail-placement-student"),
    path('detailintern/',StudentInternList.as_view(),name=  "list-intern-student"),
    path('detailintern/<str:pk>',StudentInternDetail.as_view(),name=  "detail-intern-student"),
    path('detailnotsitting/',StudentNotSittingList.as_view(),name=  "list-notsitting-student"),
    path('detailnotsitting/<str:pk>',StudentNotSittingDetail.as_view(),name=  "detail-notsitting-student"),
    path('basicstats/',BasicStats.as_view(),name = "basic-stats-info"),
    path('orderwise/',CommonQueries.as_view(),name ="stats-by-order")
   
    # path('cluster/',clusterchoosen.as_view(),name=  "detail-intern-student"),


]

