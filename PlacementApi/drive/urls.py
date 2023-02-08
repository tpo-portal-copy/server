from django.urls import path
from .views import DriveList,DriveDetail
urlpatterns = [
    path('',DriveList.as_view(),name = 'list-create-drive'),
    path('<int:pk>',DriveDetail.as_view(),name = 'detail-drive'),
]