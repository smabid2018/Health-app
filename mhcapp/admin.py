from django.contrib import admin
from .models import CustomUser, AdminProfile, DoctorProfile, NurseProfile, LabTechnicianProfile, RadiographerProfile, PatientProfile

# Register your models here.
from django.contrib import admin


admin.site.register(CustomUser)
admin.site.register(AdminProfile)
admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)
admin.site.register(LabTechnicianProfile)
admin.site.register(RadiographerProfile)
admin.site.register(PatientProfile)
