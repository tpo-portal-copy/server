from django.db import models
# from student.models import Student,Company
from drive.models import Drive,Company
from django.utils import timezone
from django.core.validators import RegexValidator
from tpr.models import TPR

# Create your models here.
class TPO(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.name + " " + self.email


# class TPR(models.Model):
#     name = models.OneToOneField(Student, on_delete=models.CASCADE)


class Announcement(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=500)
    # type = models.CharField(max_length=100)
    description = models.TextField()
    # company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    # company = models.CharField(max_length=100, blank=True, null=True)
    session = models.CharField(max_length=7,validators=[RegexValidator(regex=r'\d{4}[-]\d{2}$')])
    # time = models.DateTimeField(auto_now=True)
    tpo = models.ForeignKey(TPO, on_delete=models.CASCADE, blank=True, null=True)
    tpr = models.ForeignKey(TPR, on_delete=models.CASCADE, blank=True,null=True)
    class Meta:
        abstract = True

class GeneralAnnouncement(Announcement):
    type = models.CharField(max_length=30, choices = [('general','General'), ('results','Results')])
    def __str__(self) -> str:
        return self.title

class CompanyAnnouncement(Announcement):
    drive = models.ForeignKey(Drive, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.title

branch_choices = [
    ('cse','Computer Science and Engineering'),
    ('civil','Civil Engineering'),
    ('mech','Mechanical Engineering'),
    ('electrical','Electrical Engineering'),
    ('chemical','Chemical Engineering'),
    ('ece','Electronics and Communication Engineering'),
    ('material','Material Science and Engineering'),
    ('mnc','Mathematics and Computing'),
    ('eph','Engineering Physics'),
    ('archi','Architecture Engineering'),
    ('mba','MBA'),
    ('sciences','Master in Sciences')
]


class Resources(models.Model):
    type = models.CharField(max_length=20, choices=[('management','Management'),('sciences','Sciences'),('tech','Technical')])
    branch = models.CharField(max_length=30,choices=branch_choices)
    heading = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=[('article','Articles and Links'), ('faq','FAQs')])
    content = models.TextField()

jtype = [
    ('intern','Internship'),
    ('placement','Placement'),
    ('intern and fte', 'Internship+Placement')
]
class DriveApproved(models.Model):
    approved_date = models.DateTimeField(auto_now_add=True)
    spocs = models.ManyToManyField(TPR)
    last_date = models.DateTimeField() # last date to create drive by tpr
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    session = models.CharField(max_length=7,validators=[RegexValidator(regex=r'\d{4}[-]\d{2}$')])
    job_type = models.CharField(max_length=15, choices=jtype)

    class Meta:
        unique_together = ['company','session','job_type']
 
