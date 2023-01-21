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


# We need to fill manually
class CourseYearAllowed(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()  # denotes different years in B.Tech, M.Tech., etc..
    type_allowed = models.CharField(max_length=20, choices=[('intern', "Internship"), ('placement', "Placement"), ('NA', "Not Allowed")])