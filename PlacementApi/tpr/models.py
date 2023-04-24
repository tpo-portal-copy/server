from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TPR(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_tpr')