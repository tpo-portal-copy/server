from django.db import models
from course.models import Course,Specialization
# Create your models here.

from drive.models import Drive


    
class Country(models.Model):
    name = models.CharField(default="",max_length=100)
    def __str__(self) -> str:
        return self.name

class State(models.Model):
    name = models.CharField(default="",max_length=100)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name

class City(models.Model):
    name = models.CharField(default="",max_length=100)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name 


class School(models.Model):
    name = models.CharField(default="",max_length=200)
    board = models.CharField(default="",max_length=200)
    def __str__(self) -> str:
        return self.name

class Cluster(models.Model):
    Cluster_id = models.IntegerField(primary_key=True)
    starting = models.FloatField(default=0)
    ending = models.FloatField(default=0)

    def __str__(self) -> str:
        return str(self.Cluster_id) 

class Category(models.Model):
    name = models.CharField(primary_key=True,max_length=100)
    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    roll = models.BigIntegerField(primary_key=True)
    middle_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length = 100,blank=True,null=True)
    college_email = models.EmailField(null=False)
    personal_email = models.EmailField(null=False)
    gender = models.CharField(default="",max_length=100)
    branch = models.ForeignKey(Specialization,on_delete=models.CASCADE)
    pnumber = models.BigIntegerField()
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    pincode = models.BigIntegerField()
    batch_year = models.IntegerField()
    cluster_1 = models.ForeignKey(Cluster,on_delete=models.CASCADE,related_name = "cluster_1")
    cluster_2 = models.ForeignKey(Cluster,on_delete = models.CASCADE,related_name = "cluster_2")
    cluster_3 = models.ForeignKey(Cluster,on_delete = models.CASCADE,related_name = "cluster_3")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    resume = models.CharField(default="",max_length=200)
    undertaking = models.CharField(default="",max_length=200)
    cgpi = models.FloatField(default=0)
    class_10_year = models.IntegerField()
    # class_10_school = models.CharField(default="",max_length=200)
    # class_10_board = models.CharField(default="",max_length=200)
    class_10_perc = models.FloatField()
    class_12_year = models.IntegerField()
    # class_12_school = models.CharField(default="",max_length=200)
    # class_12_board = models.CharField(default="",max_length=200)
    class_12_perc = models.FloatField()
    active_backlog = models.SmallIntegerField()
    total_backlog = models.SmallIntegerField()
    linkedin = models.CharField(default="",max_length=200)

    def __str__(self):
        return self.first_name + self.last_name


jtype = [
 ('intern','Internship'),
 ('placement','Placement'),
]
class Recruited(models.Model):
    student = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True)
    drive = models.ForeignKey(Drive,on_delete=models.CASCADE)
    jobtype = models.CharField(choices=jtype,max_length=20)





# class Education(models.Model):
#     roll = models.ForeignKey(Student,on_delete=models.CASCADE)
#     class_name = models.SmallIntegerField(default=10,null= False)
#     school = models.ForeignKey(School,on_delete=models.CASCADE)
#     percentage = models.FloatField(default=0,null = False)

#     def __str__(self) -> str:
#         return str(self.roll) + " " + self.class_name

 