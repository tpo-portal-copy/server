from django.contrib import admin
from .models import Drive,Role,JobRoles

# Register your models here.
@admin.register(Drive)
class DriveAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('company__name',)
# admin.site.register(Role)
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    # list_display = ('id',)
    search_fields = ('name',)
# admin.site.register(JobRoles)
@admin.register(JobRoles)
class JobRolesAdmin(admin.ModelAdmin):
    # search_fields = ('',)
    search_fields = ('drive__company__name',)
    

# admin.site.register(Branchallowed)
