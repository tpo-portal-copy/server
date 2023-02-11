from django.contrib import admin
from .models import Experience
# Register your models here.
admin.site.register(Experience)
# admin.site.register(Role)
# @admin.register(Role)
# class RoleAdmin(admin.ModelAdmin):
#     search_fields = ('role',)