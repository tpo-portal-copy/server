from django.contrib import admin
from .models import Student,City,State,Country,Cluster,School,Category,ClusterChosen,Recruited,Got_PPO
# Register your models here.

admin.site.register(Student)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Cluster)
admin.site.register(School)
admin.site.register(Category)
admin.site.register(ClusterChosen)
admin.site.register(Recruited)
admin.site.register(Got_PPO)
