from django.db import models
from course.models import Specialization

# Create your models here.
class Company(models.Model):
    def company_directory_path(instance, filename):
        return 'company_logos/{0}.jpg'.format(instance.name)
    name = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to= company_directory_path, max_length=255)
    # type (IT or Core)
    def __str__(self) -> str:
        return self.name

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
        return self.company.name + " " + self.mode_of_hiring


class JNF_placement(models.Model):
    def job_desc_directory_path(instance, filename):
        return 'jnf/job_desc/placement/{0}.pdf'.format(instance.jnf.company.name + instance.job_profile)
    jnf = models.OneToOneField(JNF, on_delete=models.CASCADE)
    joining_date_placement = models.DateField()
    job_profile = models.CharField(max_length=100)
    ctc = models.FloatField() #in LPA
    job_desc_pdf = models.FileField(upload_to=job_desc_directory_path, null=True, blank=True)
    eligible_batches = models.ManyToManyField(Specialization) # add only specialisations which are eligible
    def __str__(self) -> str:
        return self.jnf.company.name + " " + self.job_profile

class JNF_intern(models.Model):
    def job_desc_directory_path(instance, filename):
        return 'jnf/job_desc/intern/{0}.pdf'.format(instance.jnf.company.name + instance.job_profile)
    jnf = models.OneToOneField(JNF, on_delete=models.CASCADE)
    has_ppo = models.BooleanField()
    duration = models.IntegerField() #in months
    tentative_start = models.DateField()
    job_profile = models.CharField(max_length=100)
    ctc = models.FloatField() #in LPA
    job_desc_pdf = models.FileField(upload_to=job_desc_directory_path, null=True, blank=True)
    eligible_batches = models.ManyToManyField(Specialization, blank=True) # add only specialisations which are eligible
    def __str__(self) -> str:
        return self.jnf.company.name + " " + self.job_profile