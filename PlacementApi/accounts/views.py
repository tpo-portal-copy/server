from django.shortcuts import redirect
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework_simplejwt.views import jwt_views
from django.http import HttpResponse  
from PlacementApi import settings  
from django.core.mail import send_mail  
  
  
def mail(request):  
    subject = "Greetings"  
    msg     = "Congratulations for your success"  
    to      = "193069@nith.ac.in"  
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
    if(res == 1):  
        msg = "Mail Sent Successfuly"  
    else:  
        msg = "Mail could not sent"  
    return HttpResponse(msg)  

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })



# class LoginAPI(KnoxLoginView):
    # permission_classes = (permissions.AllowAny,)

    # def post(self, request, format=None):
    #     serializer = AuthTokenSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     login(request, user)
    #     return super(LoginAPI, self).post(request, format=None)