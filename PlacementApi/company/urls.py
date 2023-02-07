from django.urls import path
from . import views

urlpatterns = [
    # path('',views.CompanyAPIView.as_view()),
    path('',views.CompanyListAPIView.as_view()),
    path('<str:name>',views.CompanyDetailAPIView.as_view()),
    path('<str:name>/hr/',views.HRListAPIView.as_view()),
    path('<str:name>/hr/<int:pk>/',views.HRDestroyAPIView.as_view()),
    path('add-hr/',views.HRCreateAPIView.as_view()),
    path('jnfs/',views.JNFList.as_view()),
    path('jnf/<str:company>/',views.JNFRetrieveAPIView.as_view()),
    path('jnfplacements/',views.JNFPlacementAPIView.as_view()),
    path('jnfplacements/<str:company>',views.JNFPlacementRetrieveAPIView.as_view()),
    path('jnfinterns/',views.JNFInternAPIView.as_view()),
    path('jnfinterns/<str:company>',views.JNFInternRetrieveAPIView.as_view()),
    path('add-jnf/',views.JNFCreateAPIView.as_view()),
]