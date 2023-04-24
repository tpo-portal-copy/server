from django.db import models
from django.core.validators import RegexValidator
from accounts.utils import GetSession

# Create your models here.
class Cluster(models.Model):
    cluster_id = models.IntegerField(primary_key=True)
    starting = models.FloatField(default=0)
    ending = models.FloatField(default=0)
    session = models.CharField(max_length=7,default=GetSession().CurrentSession(),validators=[RegexValidator(regex=r'\d{4}[-]\d{2}$')])

    def __str__(self) -> str:
        return str(self.cluster_id) 

class Course(models.Model):
    name = models.CharField(max_length=20, null = True)
    years = models.IntegerField(default=4,null= True)
    def __str__(self) -> str:
        return self.name 

class Specialization(models.Model):
    branchName = models.CharField(max_length=200)
    branchFullname = models.CharField(max_length=200,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    onCampus = models.IntegerField(default=75)
    offCampusPpo = models.IntegerField(default = 80)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.branchName


# We need to fill manually
class CourseYearAllowed(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()  # denotes different years in B.Tech, M.Tech., etc..
    type_allowed = models.CharField(max_length=20, choices=[('intern', "Internship"), ('placement', "Placement"), ('NA', "Not Allowed"),('completed','Completed'),('both','Both')])

    class Meta:
        unique_together = ["course","year"]
    def __str__(self) -> str:
        return self.course.name + str(self.year) + self.type_allowed