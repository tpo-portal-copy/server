from django.urls import path
from .views import DriveList,DriveDetail,RolesList,JobRoles
urlpatterns = [
    path('',DriveList.as_view(),name = 'list-create-drive'),
    path('<int:pk>',DriveDetail.as_view(),name = 'detail-drive'),
    path('getroles/',RolesList.as_view(),name = "get-roles"),
    # path('storejobroles',JobRoles.as_view(),name = "add-job-roles"),
    # path('filldataset',roll_filling,name = "flood-dataset"),
]