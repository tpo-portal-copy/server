from django.urls import path
from .views import *
urlpatterns = [

    path('',roll_filling,name = "input roles"),
]