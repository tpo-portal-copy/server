from django.urls import path
from . import views
urlpatterns = [
    path('', views.AnnouncementAPIView.as_view(), name="announcement"),
    path('resources/<str:branch>/', views.ResourceListCreateAPIView.as_view(), name="resources"),
    path('resources/<int:pk>', views.ResourceRetrieveUpdateAPIView.as_view(), name="announcement"),

]