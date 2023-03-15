from django.contrib import admin
from .models import TPO,TPR,GeneralAnnouncement,CompanyAnnouncement
# Register your models here.
admin.site.register(TPO)
admin.site.register(TPR)
admin.site.register(CompanyAnnouncement)
admin.site.register(GeneralAnnouncement)