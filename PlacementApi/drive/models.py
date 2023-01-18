from django.db import models
from company.models import Company
from course.models import Specialization
# Create your models here.

class Drive(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    ctc_offered = models.FloatField()
    name = models.CharField(max_length=100)
    starting_date = models.DateField()
    year = models.IntegerField()

class Branchallowed(models.Model):
    drive = models.ForeignKey(Drive,on_delete=models.CASCADE)
    branch = models.ForeignKey(Specialization,on_delete=models.CASCADE)
