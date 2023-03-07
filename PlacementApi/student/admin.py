from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Cluster)
admin.site.register(Category)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id']
    
# admin.site.register(StudentIntern)
@admin.register(StudentIntern)
class StudentPlacementAdmin(admin.ModelAdmin):
    list_display = ['id']
# admin.site.register(StudentPlacement)
@admin.register(StudentPlacement)
class StudentPlacementAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(StudentNotSitting)
admin.site.register(ClusterChosen)
admin.site.register(Placed)
admin.site.register(Interned)
admin.site.register(Offcampus)
admin.site.register(PPO)
