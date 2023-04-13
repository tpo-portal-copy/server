from django.contrib import admin
from .models import TPO,TPR,GeneralAnnouncement,CompanyAnnouncement,Resources,DriveApproved
# Register your models here.
admin.site.register(TPO)
# admin.site.register(TPR)
admin.site.register(CompanyAnnouncement)
admin.site.register(GeneralAnnouncement)
admin.site.register(Resources)
admin.site.register(DriveApproved)
