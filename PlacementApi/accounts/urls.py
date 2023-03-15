from .views import RegisterAPI
from django.urls import path
# from knox import views as knox_views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
     path('api/login/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
     path('api/login/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
     path('api/register/', RegisterAPI.as_view(), name='register'),
]