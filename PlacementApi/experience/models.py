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

c_type_choices = [
    ('it', "IT"),
    ('mech core', "Mechanical Core"),
    ('electrical core', 'Electrical Core'),
    ('electronics core', 'Electronics Core'),
    ('civil core', "Civil Core"),
    ('chemical core', "Chemical Core"),
    ('material core', "Material Science Core"),
    ('archi core', "Architecture Core"),
    ('other', "Others")
]
class Role(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.role 

class Experience(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    difficulty = models.CharField(choices=diff_choices,max_length=5)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    text = models.TextField()
    no_of_rounds = models.PositiveIntegerField()
    company_type = models.CharField(max_length=50, choices=c_type_choices) # denotes IT, Mech Core, etc..
    roles = models.ForeignKey(Role,on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    selected = models.BooleanField(default=False)
    anonymity = models.BooleanField(default=False)
    jobtype = models.CharField(choices=jtype,max_length=100)

