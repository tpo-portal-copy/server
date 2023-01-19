from django.contrib import admin
from .models import Company,JNF,JNF_intern,JNF_placement,HR_details
# Register your models here.

admin.site.register(Company)
admin.site.register(JNF)
admin.site.register(JNF_intern)
admin.site.register(JNF_placement)
admin.site.register(HR_details)
