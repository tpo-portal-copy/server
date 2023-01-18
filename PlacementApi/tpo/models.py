from django.db import models
from student.models import Student
from django.utils import timezone
# Create your models here.
class TPO(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class TPR(models.Model):
    name = models.ForeignKey(Student,on_delete=models.CASCADE)


class Announcement(models.Model):
    title = models.CharField(max_length=500)
    type = models.CharField(max_length=100)
    description = models.TextField()
    time = models.DateTimeField(default=timezone.now())
    tpo = models.ForeignKey(TPO,on_delete=models.CASCADE,null=True)
    tpr = models.ForeignKey(TPR,on_delete=models.CASCADE,null=True)
