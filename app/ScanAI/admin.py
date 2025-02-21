from django.contrib import admin
from app.ScanAI.models import Resonancia , PatientProfile,ResonanciaImagen,Informe,DoctorProfile


admin.site.register(Resonancia)
admin.site.register(PatientProfile)
admin.site.register(ResonanciaImagen)
admin.site.register(Informe)
admin.site.register(DoctorProfile)
