from django.db import models
from course.models import Specialization

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    # type (IT or Core)

class HR_details(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(default = 'primary', choices = [('primary','Primary'), ('secondary','Secondary')],max_length=10)
    name = models.CharField(max_length=50)
    mobile = models.BigIntegerField()
    email = models.EmailField()
    def __str__(self) -> str:
        return [self.company.name,self.type,self.name].join(" ")

class JNF(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_placement = models.BooleanField()
    is_intern = models.BooleanField()
    mode_of_hiring = models.CharField(default="virtual", choices = [('virtual','Virtual'),('onsite','On-Site')], max_length=20)
    pre_placement_talk = models.BooleanField(default=True)
    aptitude_test = models.BooleanField(default=True)
    technical_test = models.BooleanField(default=True)
    group_discussion = models.BooleanField(default=True)
    personal_interview = models.BooleanField(default=True)
    no_of_persons_visiting = models.IntegerField(default=0) # 0 if drive is virtual
    job_location = models.CharField(max_length=100) # Separate different job locations with any delimeter
    def __str__(self):
        return self.company + " " + self.mode_of_hiring


class JNF_placement(models.Model):
    jnf = models.OneToOneField(JNF, on_delete=models.CASCADE)
    joining_date_placement = models.DateField()
    job_profile = models.CharField(max_length=100)
    ctc = models.FloatField() #in LPA
    job_desc_pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)
    eligible_batches = models.ManyToManyField(Specialization) # add only specialisations which are eligible
    def __str__(self) -> str:
        return self.company + " " + self.job_profile

class JNF_intern(models.Model):
    jnf = models.OneToOneField(JNF, on_delete=models.CASCADE)
    has_ppo = models.BooleanField()
    duration = models.IntegerField() #in months
    tentative_start = models.DateField()
    job_profile = models.CharField(max_length=100)
    ctc = models.FloatField() #in LPA
    job_desc_pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)
    eligible_batches = models.ManyToManyField(Specialization) # add only specialisations which are eligible
    def __str__(self) -> str:
        return self.company + " " + self.job_profile