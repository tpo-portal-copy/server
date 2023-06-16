from django.shortcuts import redirect
from rest_framework import generics, permissions,status,views
from rest_framework.response import Response
from .serializers import RegisterSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer, ChangePasswordSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.sites.shortcuts import get_current_site
# from rest_framework_simplejwt.views import jwt_views
from .permissions import TPRPermissions,TPOPermissions
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponsePermanentRedirect
from .models import UserOtp
from .utils import MailSender
import datetime
import pytz
import random
import os
from rest_framework_simplejwt.tokens import RefreshToken

# Logout View

class LogoutView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            not_verified = User.objects.get(username = request.data["username"],isActive = False)
            # not_verified = UserOtp.objects.get(user__username = request.data["username"])
            not_verified.delete()
        except:
            pass
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()        
            otp = random.randint(100000,999999)
            userotp = UserOtp.objects.create(user=user,otp = otp)
            userotp.save()
            res = MailSender().send_otp(data={"otp":otp}, email=user.email)
            print(res)
            if res:
                return Response("otp send succesfully",status=status.HTTP_200_OK)
            else:
                return Response("otp send failed",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class OTPVerification(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        # print(user)
        username = request.data['username']
        otp = int(request.data['otp'])
        # password = request.data['password']
        try:
            user = User.objects.get(username=username, isActive = False)
            print(user)
            userotp = UserOtp.objects.get(user=user)
            print(userotp)
            if(datetime.datetime.now(pytz.utc) > userotp.time+datetime.timedelta(minutes=5)):
                return Response({"msg":"OTP Expired. Regenerate"}, status=status.HTTP_400_BAD_REQUEST)
            if otp == userotp.otp:
                user.isActive = True
                user.save()
                userotp.delete()
                MailSender().registration_success(data={"username":user.username},email=user.email)
                return Response({"msg": "College Email Verified Successfully",}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": "OTP Didn't Match",}, status=status.HTTP_201_CREATED)
        except:
            return Response({"msg":"UserName Does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class OTPResend(views.APIView):
    def post(self,request):
        username = request.data["username"]
        try:
            user = User.objects.get(username=username,isActive = False)
            otp = random.randint(100000,999999)
            userotp = UserOtp.objects.get(user=user)
            userotp.otp = otp
            userotp.save()
            res = MailSender().send_otp(data={"otp":"876123"}, email=user.email)
            if res:
                return Response("otp send succesfully",status=status.HTTP_200_OK)
            else:
                return Response("otp send failed",status=status.HTTP_400_BAD_REQUEST)    
        except:
            return Response("User does not exists !",status=status.HTTP_404_NOT_FOUND)


class CheckPermissions(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        elif self.request.method == 'POST':
            return [TPRPermissions()]
        else:
            return []
   
    def get(self,request):
        # self.permission_classes = [TPRPermissions]
        return Response("HII I AM TPR AND YOU HAVE TO LISTEN TO ME !!!",status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        print(user)

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        uidb64=urlsafe_base64_encode(force_bytes(user.pk))

        # current_site = get_current_site(request=request).domain
        absurl = request.build_absolute_uri(reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token}))
        print(absurl)

        # res = MailSender().send_otp(data={"otp":"876123"}, email=user.email)
        res = MailSender().send_password_reset_mail(data={"name":user.username, "action_url":absurl}, email=user.email)

        return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def get(self, request, uidb64, token):
        serializer = self.serializer_class(data={"uidb64":uidb64,"token":token})
        if serializer.is_valid():
            return Response({"msg":"Valid Password Reset Link. Enter the Password now"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, uidb64, token):
        password = request.data["password"]
        password2 = request.data["password2"]
        serializer = self.serializer_class(data={"uidb64":uidb64,"token":token, "password":password, "password2":password2})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg":"Password Reset Done. You can login now"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()

            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)