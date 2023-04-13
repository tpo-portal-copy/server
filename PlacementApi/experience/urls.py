from django.urls import path
from . import views
urlpatterns = [
    path('',views.ExperienceList.as_view(),name = "experience-list"),
    path('<int:pk>',views.ExperienceDetail.as_view(),name = "experience-detail"),
    path('my-experiences/',views.StudentExperience.as_view(),name = "student-experiences"),

]