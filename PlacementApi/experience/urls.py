from django.urls import path
from .views import *
urlpatterns = [
    path('',ExperienceList.as_view(),name = "experience-list"),
    path('<int:pk>',ExperienceDetail.as_view(),name = "experience-detail"),

]