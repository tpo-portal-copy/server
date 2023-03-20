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
    search_fields = ["roll__username"]
    
# admin.site.register(StudentIntern)
@admin.register(StudentIntern)
class StudentInternAdmin(admin.ModelAdmin):
    search_fields = ["student__roll__username"]

    # list_display = ['id']
# admin.site.register(StudentPlacement)
@admin.register(StudentPlacement)
class StudentPlacementAdmin(admin.ModelAdmin):
    search_fields = ["student__roll__username"]

admin.site.register(StudentNotSitting)
admin.site.register(ClusterChosen)
@admin.register(Placed)
class StudentPlacedAdmin(admin.ModelAdmin):
    search_fields = ["job_role__drive__session"]

@admin.register(Interned)
class StudentInternedAdmin(admin.ModelAdmin):
    search_fields = ["student__student__course__name"]
admin.site.register(Offcampus)
admin.site.register(PPO)
