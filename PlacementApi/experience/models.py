from django.db import models
from company.models import Company
from student.models import Student
# Create your models here.
diff_choices = [
    ('E' ,'Easy'),
    ('M' , 'Medium'),
    ('H' , 'Hard')
]
jtype = [
 ('intern','Internship'),
 ('placement','Placement'),
]
class Experience(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    difficulty = models.CharField(choices=diff_choices,max_length=5)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField()
    selected = models.BooleanField(default=False)
    anonymity = models.BooleanField(default=False)
    jobtype = models.CharField(choices=jtype,max_length=100)

