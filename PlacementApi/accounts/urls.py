from .views import RegisterAPI
from django.urls import path
# from knox import views as knox_views
from rest_framework_simplejwt import views as jwt_views
# urlpatterns = [
#     path('api/register/', RegisterAPI.as_view(), name='register'),
#     path('api/login/', LoginAPI.as_view(), name='login'),
#     path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
#     path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
# ]
urlpatterns = [
    path('student/login/',
         jwt_views.TokenObtainPairView.as_view(),
         name ='token_obtain_pair'),
    path('student/login/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name ='token_refresh'),
    path('register/', RegisterAPI.as_view(), name='register'),
]