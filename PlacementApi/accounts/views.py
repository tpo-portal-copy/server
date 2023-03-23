from django.shortcuts import redirect
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import permissions,generics,views
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework_simplejwt.views import jwt_views
from django.http import HttpResponse  
from PlacementApi import settings  
from django.core.mail import send_mail  
from .permissions import TPRPermissions,TPOPermissions
from django.contrib.auth.models import User
from .models import UserOtp
import datetime
import pytz
import random
  
  
def MailSender(otp,email):  
    subject = "NITH Placement Portal Verification"
    msg = f"Your OTP is {otp}"
    to = email
    res = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    return res

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            not_verified = User.objects.get(username = request.data["username"],is_active = False)
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
            res = MailSender(otp,user.email)
            if res:
                return Response("otp send succesfully",status=status.HTTP_200_OK)
            else:
                return Response("otp send failed",status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


class OTPVerification(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        print(request.data)
        # print(user)
        username = request.data['username']
        otp = int(request.data['otp'])
        # password = request.data['password']
        try:
            user = User.objects.get(username=username, is_active = False)
            userotp = UserOtp.objects.get(user=user)            
            if(datetime.datetime.now(pytz.utc) > userotp.time+datetime.timedelta(minutes=5)):
                return Response({"msg":"OTP Expired. Regenerate"}, status=status.HTTP_400_BAD_REQUEST)
            if otp == userotp.otp:
                user.is_active = True
                user.save()
                userotp.delete()
                send_mail("NITH Placement Portal Registeration","You are Now Successfully Register with NITH Placement Portal",settings.EMAIL_HOST_USER, [user.email])
                return Response({"msg": "College Email Verified Successfully",}, status=status.HTTP_201_CREATED)
            else:
                return Response({"msg": "OTP Didn't Match",}, status=status.HTTP_201_CREATED)
        except:
            return Response({"msg":"UserName Does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class OTPResend(views.APIView):
    def post(self,request):
        username = request.data["username"]
        try:
            user = User.objects.get(username=username,is_active = False)
            otp = random.randint(100000,999999)
            userotp = UserOtp.objects.get(user=user)
            userotp.otp = otp
            userotp.save()
            res = MailSender(otp,user.email)
            if res:
                return Response("otp send succesfully",status=status.HTTP_200_OK)
            else:
                return Response("otp send failed",status=status.HTTP_400_BAD_REQUEST)    
        except:
            return Response("User does not exists !",status=status.HTTP_404_NOT_FOUND)




        








    


class CheckPermissions(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated,TPRPermissions]
    def get(self,request):
        return Response("HII I AM TPR AND YOU HAVE TO LISTEN TO ME !!!",status=status.HTTP_200_OK)


    
