from django.db import models

# Create your models here.
class Cluster(models.Model):
    cluster_id = models.IntegerField(primary_key=True)
    starting = models.FloatField(default=0)
    ending = models.FloatField(default=0)

    def __str__(self) -> str:
        return str(self.cluster_id) 

class Course(models.Model):
    name = models.CharField(max_length=20, null = True)
    years = models.IntegerField(default=4,null= True)
    def __str__(self) -> str:
        return self.name

class Specialization(models.Model):
    branch_name = models.CharField(max_length=200)
    branch_fullname = models.CharField(max_length=200,null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return self.branch_name


# We need to fill manually
class CourseYearAllowed(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()  # denotes different years in B.Tech, M.Tech., etc..
    type_allowed = models.CharField(max_length=20, choices=[('intern', "Internship"), ('placement', "Placement"), ('NA', "Not Allowed"),('completed','Completed'),('both','Both')])

    class Meta:
        unique_together = ["course","year"]