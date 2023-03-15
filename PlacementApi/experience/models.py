from django.db import models
from company.models import Company
from student.models import Student
from drive.models import Role
# from django_quill.fields import QuillField

# Create your models here.
diff_choices = [
    ('E' ,'Easy'),
    ('M' , 'Medium'),
    ('H' , 'Hard')
]
jtype = [
    ('Internship','Internship'),
    ('Placement','Placement'),
]

# c_type_choices = [
#     ('it', "IT"),
#     ('mech core', "Mechanical Core"),
#     ('electrical core', 'Electrical Core'),
#     ('electronics core', 'Electronics Core'),
#     ('civil core', "Civil Core"),
#     ('chemical core', "Chemical Core"),
#     ('material core', "Material Science Core"),
#     ('archi core', "Architecture Core"),
#     ('other', "Others")
# ]

class Experience(models.Model):
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    difficulty = models.CharField(choices=diff_choices,max_length=5)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    description = models.TextField()
    no_of_rounds = models.PositiveIntegerField()
    roles = models.ForeignKey(Role,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    selected = models.BooleanField(default=False)
    anonymity = models.BooleanField(default=False)
    jobtype = models.CharField(choices=jtype,max_length=100)

