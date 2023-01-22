from django.contrib import admin
from .models import Course,Specialization,CourseYearAllowed
# Register your models here.

admin.site.register(Course)
admin.site.register(CourseYearAllowed)
admin.site.register(Specialization)
