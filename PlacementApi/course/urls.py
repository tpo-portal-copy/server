from django.urls import path
from . import views

urlpatterns = [
    path('',views.CourseAPIView.as_view()),
    path('specializations/',views.SpecializationAPIView.as_view()),
    path('branches/<int:id>',views.SpecilizationDetailAPIView.as_view()),
    path('course-year-allowed/',views.CourseYearAllowedAPIView.as_view()),
]