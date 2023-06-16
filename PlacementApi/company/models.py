from django.db import models
from course.models import Specialization
from validators import Validate_file_size
from django.core.validators import RegexValidator, FileExtensionValidator, MaxValueValidator

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
    mobile = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^(\+91)?[6-9]\d{9}$')])
    email = models.EmailField()
    def __str__(self) -> str:
        return f"{self.company.name} {self.type} {self.name}"

    class Meta:
        unique_together = ("company", "type")

# custom model manager for excluding banned student
class JNFManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isApproved = True) 

class JNF(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company")
    session = models.CharField(max_length=7,validators=[RegexValidator(regex=r'\d{4}[-]\d{2}$')])
    isPlacement = models.BooleanField()
    isIntern = models.BooleanField()
    isSixMonthsIntern = models.BooleanField(default=False) 
    modeOfHiring = models.CharField(default="virtual", choices = [('virtual','Virtual'),('onsite','On-Site'),('hybrid','Hybrid')], max_length=20)
    prePlacementTalk = models.BooleanField(default=True)
    aptitudeTest = models.BooleanField(default=True)
    technicalTest = models.BooleanField(default=True)
    groupDiscussion = models.BooleanField(default=True)
    personalInterview = models.BooleanField(default=True)
    noOfPersonsVisiting = models.IntegerField(default=0) # 0 if drive is virtual
    jobLocation = models.CharField(max_length=100) # Separate different job locations with any delimeter
    tentativeDriveDate = models.DateField()
    # hr = models.ManyToManyField(HR_details, blank=True)
    isApproved = models.BooleanField(default=False)

    objects = models.Manager()
    approved = JNFManager()
    def __str__(self):
        return self.company.name + " " + self.modeOfHiring

    class Meta:
        unique_together = ("company", "session")


class JNF_placement_base(models.Model):
    def job_desc_directory_path(instance, filename):
        return 'jnf/job_desc/placement/{0}.pdf'.format(instance.jnf.company.name + instance.jobProfile)
    tentativeJoiningDate = models.DateField()
    jobProfile = models.CharField(max_length=100)
    jobDescPdf = models.FileField(upload_to=job_desc_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['docx','doc','pdf']), Validate_file_size(5,"MB")])
    cgpi = models.FloatField(validators=[MaxValueValidator(10)])
    eligibleBatches = models.ManyToManyField(Specialization) # add only specialisations which are eligible
    class Meta:
        abstract = True
        unique_together = ['jnf','jobProfile']

class JNF_placement(JNF_placement_base):
    jnf = models.ForeignKey(JNF, on_delete=models.CASCADE, related_name="jnfPlacement")
    hasIntern = models.BooleanField(default=False)
    ctc = models.FloatField() #in LPA


class JNF_intern_fte(JNF_placement_base):
    jnf = models.ForeignKey(JNF, on_delete=models.CASCADE, related_name="jnfInternFte")
    ctcAfterIntern = models.FloatField() #in LPA
    stipend = models.FloatField() #in thousands
    duration = models.PositiveIntegerField(default=6)


class JNF_intern(models.Model):
    def job_desc_directory_path(instance, filename):
        return 'jnf/job_desc/intern/{0}.pdf'.format(instance.jnf.company.name + instance.jobProfile)
    jnf = models.ForeignKey(JNF, on_delete=models.CASCADE, related_name="jnfIntern")
    hasPpo = models.BooleanField()
    duration = models.IntegerField(choices=[(1,"One Month"), (2, "Two Months")]) #in months
    tentativeJoiningDate = models.DateField()
    jobProfile = models.CharField(max_length=100)
    stipend = models.FloatField() # stipend to be given per month in thousands
    ctcAfterPpo = models.FloatField()  # expected ctc to be given if 
    jobDescPdf = models.FileField(upload_to=job_desc_directory_path, null=True, blank=True, validators=[FileExtensionValidator(['docx','doc','pdf']), Validate_file_size(5,"MB")])
    cgpi = models.FloatField(validators=[MaxValueValidator(10)])  # default cgpi puchni h
    eligibleBatches = models.ManyToManyField(Specialization, blank=True) # add only specialisations which are eligible

    class Meta:
        unique_together = ['jnf','jobProfile']
    def __str__(self) -> str:
        return self.jnf.company.name + " " + self.jobProfile
