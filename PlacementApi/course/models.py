from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class Specialization(models.Model):
    branch_name = models.CharField(max_length=200)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return self.branch_name + " " + self.course.name
