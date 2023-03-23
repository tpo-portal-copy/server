from django.db import models
from course.models import Cluster,Course,Specialization
from company.models import Company
from drive.models import JobRoles, Role
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator ,MinValueValidator,MaxValueValidator
from validators import Validate_file_size
from drive.models import Drive
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(default="",max_length=100)
    def __str__(self) -> str:
        return self.name

class State(models.Model):
    name = models.CharField(default="",max_length=100)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name

class City(models.Model):
    name = models.CharField(default="",max_length=100)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name


# class School(models.Model):
#     name = models.CharField(default="",max_length=200)
#     board = models.CharField(default="",max_length=200)
#     def __str__(self) -> str:
#         return self.name

# class Cluster(models.Model):
#     Cluster_id = models.IntegerField(primary_key=True)
#     starting = models.FloatField(default=0)
#     ending = models.FloatField(default=0)

#     def __str__(self) -> str:
#         return str(self.Cluster_id) 

# to be filled manually and denotes category like OBC, Gen, Gen-EWS , etc..
class Category(models.Model):
    name = models.CharField(primary_key=True,max_length=100)
    def __str__(self) -> str:
        return self.name

gender_types = [
    ('m','Male'),
    ('f','Female'),
    ('o','Others')
]
# custom model manager for excluding banned student
class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(banned_date__lte=timezone.now(), over_date__gte=timezone.now()) 

class Student(models.Model):
    def student_image_directory_path(instance, filename):
        return 'student/{0}/{1}.jpg'.format(instance.batch_year,instance.roll.username)
    roll = models.OneToOneField(User,on_delete=models.CASCADE,related_name="student")
    image_url = models.ImageField(upload_to =student_image_directory_path, max_length=255, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png']), Validate_file_size(10,"MB")],null=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length = 100,blank=True,null=True)
    personal_email = models.EmailField(null=False)
    gender = models.CharField(default="m", choices = gender_types, max_length=1)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    branch = models.ForeignKey(Specialization,on_delete=models.CASCADE)
    pnumber = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^(\+91)?[6-9]\d{9}$')])
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    pincode = models.BigIntegerField()
    dob = models.DateField(null=True)
    batch_year = models.IntegerField(validators=[RegexValidator(regex=r'\d{4}$')]) # for starting year at clg
    current_year = models.IntegerField(validators=[RegexValidator(regex=r'\d{1}$')])  # choices to be extracted from CourseYearAllowed table at frontend
    passing_year = models.IntegerField(validators=[RegexValidator(regex=r'\d{4}$')])
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    cgpi = models.FloatField(validators=[MaxValueValidator(10)])
    gate_score = models.FloatField(blank=True, null= True)
    cat_score = models.FloatField(blank=True, null = True)
    class_10_year = models.IntegerField(validators=[RegexValidator(regex=r'\d{4}$')])
    class_10_school = models.CharField(default="",max_length=200)
    class_10_board = models.CharField(default="",max_length=200)
    class_10_perc = models.FloatField()
    class_12_year = models.IntegerField(validators=[RegexValidator(regex=r'\d{4}$')])
    class_12_school = models.CharField(default="",max_length=200)
    class_12_board = models.CharField(default="",max_length=200)
    class_12_perc = models.FloatField()
    class_12_domicile = models.ForeignKey(State, on_delete=models.CASCADE)
    active_backlog = models.SmallIntegerField()
    total_backlog = models.SmallIntegerField()
    jee_mains_rank = models.IntegerField(null= True) 
    linkedin = models.CharField(default="",max_length=200)
    pwd = models.BooleanField(default=False)
    disability_type = models.CharField(max_length=50,choices=[('NONE','None'),('HEARING_IMPAIRMENT', 'Hearing Impairment'),('VISUAL_IMPAIRMENT', 'Visual Impairment'),('MOBILITY_IMPAIRMENT', 'Mobility Impairment'),('SPEECH_IMPAIRMENT', 'Speech Impairment'),('COGNITIVE_IMPAIRMENT', 'Cognitive Impairment'),('OTHER', 'Other')])
    disability_percentage = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    gap_12_ug = models.IntegerField(default=0)
    gap_ug_pg = models.IntegerField(default=0)
    banned_date = models.DateTimeField(default=timezone.now)
    over_date = models.DateTimeField(default=timezone.now)
    

    objects = models.Manager()
    banned = StudentManager()
    def __str__(self) -> str:
        return self.roll.username

class StudentPlacement(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE,related_name='student_placement')
    resume = models.CharField(default="",max_length=200)
    undertaking = models.BooleanField()

    def __str__(self) -> str:
        return self.student.roll.username

class StudentIntern(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE ,related_name='student_intern')
    resume = models.CharField(default="",max_length=200)
    def __str__(self) -> str:
        return self.student.roll.username

reasons = [
    ('higher studies', "Higher Studies"),
    ('research', "Research"),
    ('govt job', "Government Jobs"),
    ('enterprenuer', "Enterprenuer"),
    ('other', "Others")
]
class StudentNotSitting(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_ns')
    reason = models.CharField(max_length=40, choices=reasons)
    def __str__(self) -> str:
        return self.student.roll.username
    

class ClusterChosen(models.Model):
    student = models.OneToOneField(StudentPlacement,on_delete=models.CASCADE,related_name="cluster")
    cluster_1 = models.ForeignKey(Cluster,on_delete=models.CASCADE,related_name = "cluster_1")
    cluster_2 = models.ForeignKey(Cluster,on_delete = models.CASCADE,related_name = "cluster_2")
    cluster_3 = models.ForeignKey(Cluster,on_delete = models.CASCADE,related_name = "cluster_3")
    def __str__(self):
        return self.student.student.roll.username



class Recruited(models.Model):
    # drive = models.ForeignKey(Drive,on_delete=models.CASCADE)
    job_role = models.ForeignKey(JobRoles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# This Table is only for oncampus placed students and PPO both
class Placed(Recruited):
    student = models.ForeignKey(StudentPlacement,on_delete=models.CASCADE)
    def __str__(self):
        return self.student.student.roll.username


class Interned(Recruited):
    student = models.ForeignKey(StudentIntern,on_delete=models.CASCADE)
    def __str__(self):
        return self.student.student.roll.username   



class BaseClass(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    ctc = models.FloatField() # in LPA
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    session = models.CharField(max_length=7,validators=[RegexValidator(regex=r'\d{4}[-]\d{2}$')])
    profile = models.ForeignKey(Role, on_delete=models.CASCADE)
    class Meta:
        abstract = True


class PPO(BaseClass):
    pass
# For Offcampus placements
class Offcampus(BaseClass):
    # Add the company in Company Table if it does not exist in case of Offcampus placements
    type = models.CharField(max_length=20, choices= [('intern','Internship'),('placement','Placement')])
    pass

