from django.db import models
from course.models import Specialization
from validators import Validate_file_size
from django.core.validators import RegexValidator, FileExtensionValidator, MaxValueValidator
from django.dispatch import receiver

import os

# Create your models here.
class Company(models.Model):
    def company_directory_path(instance, filename):
        print(instance.logo)
        return 'company_logos/{0}.png'.format(instance.name)

    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to= company_directory_path, null = True, max_length=255, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png','svg']),Validate_file_size(10,"MB")])
    # type (IT or Core)
    def __str__(self) -> str:
        return self.name

    def delete(self, using=None, keep_parents=False):
        print("Delete function invoked")
        storage = self.logo.storage
        if storage.exists(self.logo.name):
            storage.delete(self.logo.name)
        return super().delete(using, keep_parents)

class HR_details(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(default = 'primary', choices = [('primary','Primary'), ('secondary','Secondary')],max_length=10)
    name = models.CharField(max_length=50)
    mobile = models.BigIntegerField(validators=[RegexValidator(regex=r'^(\+91)?[6-9]\d{9}$')])
    email = models.EmailField()
    def __str__(self) -> str:
        return f"{self.company.name} {self.type} {self.name}"

    class Meta:
        unique_together = ("company", "type")

# custom model manager for excluding banned student
class JNFManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_approved = True) 

class JNF(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jnf")
    session = models.CharField(max_length=7,validators=[RegexValidator(regex=r'\d{4}[-]\d{2}$')])
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
    tentative_drive_date = models.DateField()
    # hr = models.ManyToManyField(HR_details, blank=True)
    is_approved = models.BooleanField(default=False)

    objects = models.Manager()
    approved = JNFManager()
    def __str__(self):
        return self.company.name + " " + self.mode_of_hiring

    class Meta:
        unique_together = ("company", "session")

class JNF_placement(models.Model):
    def job_desc_directory_path(instance, filename):
        return 'jnf/job_desc/placement/{0}.pdf'.format(instance.jnf.company.name + instance.job_profile)
    jnf = models.OneToOneField(JNF, on_delete=models.CASCADE, related_name="jnf_placement", unique=True)
    tentative_start = models.DateField()
    job_profile = models.CharField(max_length=100)
    ctc = models.FloatField() #in LPA
    job_desc_pdf = models.FileField(upload_to=job_desc_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['docx','doc','pdf']), Validate_file_size(5,"MB")])
    cgpi = models.FloatField(validators=[MaxValueValidator(10)])
    eligible_batches = models.ManyToManyField(Specialization) # add only specialisations which are eligible
    def __str__(self) -> str:
        return self.jnf.company.name + " " + self.job_profile

class JNF_intern(models.Model):
    def job_desc_directory_path(instance, filename):
        return 'jnf/job_desc/intern/{0}.pdf'.format(instance.jnf.company.name + instance.job_profile)
    jnf = models.OneToOneField(JNF, on_delete=models.CASCADE, related_name="jnf_intern", unique=True)
    has_ppo = models.BooleanField()
    duration = models.IntegerField() #in months
    tentative_start = models.DateField()
    job_profile = models.CharField(max_length=100)
    stipend = models.FloatField() # stipend to be given per month in thousands
    ctc = models.FloatField()  # expected ctc to be given if 
    job_desc_pdf = models.FileField(upload_to=job_desc_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['docx','doc','pdf']), Validate_file_size(5,"MB")])
    cgpi = models.FloatField(validators=[MaxValueValidator(10)])  # default cgpi puchni h
    eligible_batches = models.ManyToManyField(Specialization, blank=True) # add only specialisations which are eligible
    def __str__(self) -> str:
        return self.jnf.company.name + " " + self.job_profile


@receiver(models.signals.post_delete, sender=JNF_placement)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `JNF_placement` object is deleted.
    """
    if instance.job_desc_pdf:
        if os.path.isfile(instance.job_desc_pdf.path):
            os.remove(instance.job_desc_pdf.path)

@receiver(models.signals.pre_save, sender=JNF_placement)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `JNF_placement` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = JNF_placement.objects.get(pk=instance.pk).job_desc_pdf
    except JNF_placement.DoesNotExist:
        return False

    new_file = instance.job_desc_pdf
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)