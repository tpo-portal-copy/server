from django.urls import path
from . import views

urlpatterns = [
    # path('',views.CompanyAPIView.as_view()),
    path('',views.CompanyListAPIView.as_view()),
    path('<str:name>',views.CompanyDetailAPIView.as_view()),
    path('<str:name>/hr/',views.HRListAPIView.as_view()),
    path('<str:name>/hr/<int:pk>',views.HRDestroyAPIView.as_view()),
    path('add-hr/',views.HRCreateAPIView.as_view()),
    path('jnf/',views.JNFList.as_view()),
    path('add-jnf/',views.JNFCreateAPIView.as_view()),
]