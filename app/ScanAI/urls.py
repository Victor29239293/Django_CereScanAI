# myapp/urls.py
from django.urls import path
from app.ScanAI.view.base import DashboardView
from app.ScanAI.view.modules.analisis_resonancias import AnalisisView,UploadResonanciaView
from app.ScanAI.view.modules.informes import InformeView, ViewFileViews,generate_pdf_report
from app.ScanAI.view.modules.estadisticas import EstadisticasView
from django.conf.urls.static import static
from django.conf import settings

app_name = 'ScanAI' 
urlpatterns = [
    path('analisis/', DashboardView.as_view(), name='analisis'),
    path('AnalisisView/', AnalisisView.as_view(), name='AnalisisView'),
    path('upload-resonance/<int:pk>/', UploadResonanciaView.as_view(), name='upload_resonance'),
    
    path('gestion_informe/', InformeView.as_view(), name='gestion_informe'),
    path('view_informe/<int:paciente_id>/', ViewFileViews.as_view(), name='view_informe'),
    path('view_estadisticas/', EstadisticasView.as_view(), name='view_estadisticas'),
    
    
    path('pdf-report/<int:patient_id>/<int:resonancia_id>/', generate_pdf_report, name='generate_pdf_report'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
