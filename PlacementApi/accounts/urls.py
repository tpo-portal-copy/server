from .views import RegisterAPI
from django.urls import path
# from knox import views as knox_views
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
     path('api/login/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
     path('api/login/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
     path('api/register/', RegisterAPI.as_view(), name='register'),  
     path('api/istpr',views.CheckPermissions.as_view()),
     path('api/otp/verify/',views.OTPVerification.as_view()),
     path('api/otp/resend/',views.OTPResend.as_view()),
     path('api/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
     path('api/password-reset/',views.RequestPasswordResetEmail.as_view(),name="password-reset"),
     path('api/password-reset-confirm/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
     path('api/logout/', views.LogoutView.as_view(), name='auth_logout'),
]