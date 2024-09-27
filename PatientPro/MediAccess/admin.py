from django.contrib import admin
from .models import CustomUser, PatientRecord, Department

admin.site.register(CustomUser)
admin.site.register(PatientRecord)
admin.site.register(Department)
