from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserOtp(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    otp = models.IntegerField()
    time = models.DateTimeField(auto_now=True)
    