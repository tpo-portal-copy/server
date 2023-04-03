from django.contrib import admin
from .models import Company,HR_details,JNF,JNF_intern,JNF_intern_fte,JNF_placement
# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('name',)
admin.site.register(JNF)
admin.site.register(JNF_intern)
admin.site.register(JNF_placement)
admin.site.register(JNF_intern_fte)
admin.site.register(HR_details)
