from django.db import models
from company.models import Company
from course.models import Specialization
# Create your models here.

jtype = [
    ('intern','Internship'),
    ('placement','Placement'),
    ('intern and ppo', 'Internship + Placement')
]
class Drive(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    ctc_offered = models.FloatField()
    name = models.CharField(max_length=100)
    job_desc = models.CharField(max_length=100)   # Stores slug of the job description pdf from JNF
    starting_date = models.DateField()
    # drive type based on company type for e.g. IT, Mech Core, EE Core, etc..
    year = models.IntegerField()  # graduation year
    job_type = models.CharField(max_length=10, choices=jtype)
    eligible_batches = models.ManyToManyField(Specialization) # add only specialisations which are eligible

# class Branchallowed(models.Model):
#     drive = models.ForeignKey(Drive,on_delete=models.CASCADE)
#     branch = models.ForeignKey(Specialization,on_delete=models.CASCADE)
