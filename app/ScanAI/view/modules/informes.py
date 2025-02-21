from django.views.generic import TemplateView
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import PermissionMixin
from app.ScanAI.models import PatientProfile ,Resonancia 
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.utils import timezone
from django.contrib.auth.decorators import login_required

class InformeView(PermissionMixin, TemplateView):
    template_name = "Dashboard/modules/Gestion_Informe/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name="DOCTOR").exists():
            pacientes_con_resonancias = PatientProfile.objects.filter(user__resonancias__isnull=False).distinct()
        elif user.groups.filter(name="PACIENTE").exists():
            pacientes_con_resonancias = PatientProfile.objects.filter(user=user, user__resonancias__isnull=False).distinct()
        else:
            print('Algun error hay')
        context['pacientes_con_resonancias'] = pacientes_con_resonancias
        MenuModule(self.request).fill(context)
        return context



class ViewFileViews(TemplateView):
    template_name = "Dashboard/modules/Gestion_Informe/views_file.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        

        paciente_id = self.kwargs.get('paciente_id')
        paciente = get_object_or_404(PatientProfile, id=paciente_id)
        
       
        resonancias = paciente.user.resonancias.all()  
    
        context['paciente'] = paciente
        context['resonancias'] = resonancias
        
        MenuModule(self.request).fill(context)
        return context

def generate_pdf_report(request, patient_id, resonancia_id):
    patient = PatientProfile.objects.get(id=patient_id)
    current_date = timezone.now()
    try:
        resonance = patient.user.resonancias.get(id=resonancia_id)  
    except Resonancia.DoesNotExist:
      
        return HttpResponse("Resonancia no encontrada", status=404)

    resonance.images = [
        request.build_absolute_uri(imagen.imagen.url)
        for imagen in resonance.imagenes.all()
    ]

    html_string = render_to_string(
        'Dashboard/modules/Gestion_Informe/patient_report.html',
        {'patient': patient, 'resonances': [resonance], 'current_date': current_date}  
    )

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Resonancia_{resonancia_id}.pdf"'
    return response

