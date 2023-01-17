from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(default="",max_length=100)
    roll = models.BigIntegerField(primary_key=True)
    
class Country(models.Model):
    name = models.CharField(default="",max_length=100,null=False)

class State(models.Model):
    name = models.CharField(default="",max_length=100,null = False)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

class City(models.Model):
    name = models.CharField(default="",max_length=100,null = False)
    state = models.ForeignKey(State,on_delete=models.CASCADE)


class School(models.Model):
    name = models.CharField(default="",null = False)
    board = models.CharField(default="",null=False)


class Education(models.Model):
    roll = models.ForeignKey(Student,on_delete=models.CASCADE)
    class_name = models.SmallIntegerField(default=10,null= False)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    percentage = models.FloatField(default=0,null = False)

