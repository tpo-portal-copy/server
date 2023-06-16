from django.urls import path
from . import views
urlpatterns = [
    path('', views.AnnouncementAPIView.as_view(), name="announcement"),
    path('resources/<str:branch>/', views.ResourceListCreateAPIView.as_view(), name="resources"),
    path('resources/<int:pk>', views.ResourceRetrieveUpdateAPIView.as_view(), name="announcement"),
    path('basicstats/',views.CollegePlacementStats.as_view(),name = 'college-basics-stats'),
    path('companystats/',views.CompanyWiseStats.as_view(),name ="stats-company-wise"),
    path('studentwisestats/',views.StudentWiseStats.as_view(),name ="stats-student-wise"),


]