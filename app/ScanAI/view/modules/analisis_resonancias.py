from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from datetime import datetime

import tempfile
from app.security.mixins.mixins import PermissionMixin
from app.security.instance.menu_module import MenuModule
from app.ScanAI.models import PatientProfile, Resonancia ,ResonanciaImagen ,Informe 
from app.ScanAI.form.ResonanceImageForm import ResonanciaForm  
import os
from pathlib import Path
from django.conf import settings
from app.ScanAI.utils.analyze_resonancy import   process_flair_t1ce, create_segmentation_images
from django.core.files.base import ContentFile
import base64
import numpy as np
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import io
from django.contrib.auth.decorators import login_required


class AnalisisView(PermissionMixin, TemplateView):
    template_name = "Dashboard/modules/Analisis_resonancias/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', None)
        
        if query:
            pacientes = PatientProfile.objects.filter(
                Q(user__first_name__icontains=query) | 
                Q(user__last_name__icontains=query) | 
                Q(user__dni__icontains=query)
            )
        else:
            pacientes = PatientProfile.objects.all()

        paginator = Paginator(pacientes, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = self.get_context_data(**kwargs)
        context['pacientes'] = page_obj

        return render(request, self.template_name, context)

class UploadResonanciaView(PermissionMixin, TemplateView):
    template_name = "Dashboard/modules/Analisis_resonancias/upload_resonancia.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        context['form'] = ResonanciaForm()
        
        paciente_id = self.kwargs.get('pk')
        if paciente_id:
            paciente = get_object_or_404(
                PatientProfile.objects.select_related('user'),
                id=paciente_id
            )
            context['paciente'] = paciente
        else:
            messages.error(self.request, "No se proporcionó ID de paciente.")
            context['paciente'] = None
            
        return context

    def post(self, request, *args, **kwargs):
        try:
            confirm_save = request.POST.get('confirm_save', None)
            paciente_id = kwargs.get('pk')

            if not paciente_id:
                messages.error(request, "ID de paciente no proporcionado")
                return self.render_to_response(self.get_context_data())

            paciente_profile = get_object_or_404(
                PatientProfile.objects.select_related('user'),
                id=paciente_id
            )
            paciente = paciente_profile.user

   
            flair_path = request.session.get('flair_path')
            t1ce_path = request.session.get('t1ce_path')

            if not flair_path or not t1ce_path:
                flair_file = request.FILES.get('flair')
                t1ce_file = request.FILES.get('t1ce')

                if not all([flair_file, t1ce_file]):
                    messages.error(request, "Debes subir ambos archivos FLAIR y T1CE")
                    return self.render_to_response(self.get_context_data())

                flair_path = default_storage.save(f'temp/{flair_file.name}', flair_file)
                t1ce_path = default_storage.save(f'temp/{t1ce_file.name}', t1ce_file)

                request.session['flair_path'] = flair_path
                request.session['t1ce_path'] = t1ce_path

         
            if not default_storage.exists(flair_path) or not default_storage.exists(t1ce_path):
                messages.error(request, "Los archivos no están disponibles.")
                return self.render_to_response(self.get_context_data())

            flair_img, t1ce_img, segmentation = process_flair_t1ce(
                default_storage.path(flair_path),
                default_storage.path(t1ce_path)
            )
            result_image_b64_dict = create_segmentation_images(flair_img, t1ce_img, segmentation)

            processed_images = []
            if result_image_b64_dict:
                for key, image_b64 in result_image_b64_dict.items():
                    if image_b64:
                        result_image_content = ContentFile(base64.b64decode(image_b64))
                        result_image_name = f'procesadas/{key}_result_{paciente.id}.png'
                        saved_image_path = default_storage.save(result_image_name, result_image_content)
                        
                        if default_storage.exists(saved_image_path):
                            image_url = default_storage.url(saved_image_path)
                            processed_images.append(image_url)

            labels = {0: 'NOT tumor', 1: 'NECROTIC/CORE', 2: 'EDEMA', 3: 'ENHANCING'}
            unique_classes = np.unique(segmentation)
            detected_anomalies = [labels[label] for label in unique_classes if label != 0]

            if detected_anomalies:
                tipo_anomalia = "Anomalia Detectada"
                severity_score = (
                    (np.sum(segmentation == 1) * 0.3) +
                    (np.sum(segmentation == 2) * 0.2) +
                    (np.sum(segmentation == 3) * 0.5)
                ) / segmentation.size

                num_anomalies = len(detected_anomalies)
                if severity_score > 0.1 or num_anomalies >= 3:
                    severidad_anomalia = "Alta"
                elif severity_score > 0.05 or num_anomalies == 2:
                    severidad_anomalia = "Moderada"
                else:
                    severidad_anomalia = "Baja"
            else:
                tipo_anomalia = "No se detectaron anomalías"
                severidad_anomalia = "Ninguna"

            context = self.get_context_data()
            context['processed_images'] = processed_images
            context['tipo_anomalia'] = tipo_anomalia
            context['severidad_anomalia'] = severidad_anomalia
            context['detected_anomalies'] = detected_anomalies

            if confirm_save:
                resonancia = Resonancia(
                    paciente=paciente,
                    flair=flair_path,
                    t1ce=t1ce_path,
                    fecha=datetime.today(),
                    tipo_anomalia=tipo_anomalia,
                    severidad_anomalia=severidad_anomalia,
                )
                resonancia.save()

                for image_url in processed_images:
                    result_image_name = os.path.basename(image_url)
                    image_path = os.path.join(default_storage.location, 'procesadas', result_image_name)
                    with open(image_path, 'rb') as f:
                        resonancia_imagen = ResonanciaImagen(resonancia=resonancia)
                        resonancia_imagen.imagen.save(result_image_name, ContentFile(f.read()))

                Informe.objects.create(
                    resonancia=resonancia,
                    recomendaciones_adicionales="Considerar seguimiento mensual."
                )

                request.session.pop('flair_path', None)
                request.session.pop('t1ce_path', None)
                messages.success(request, "La información ha sido guardada exitosamente.")
                return redirect('ScanAI:AnalisisView')

            return self.render_to_response(context)

        except Exception as e:
            messages.error(request, f"Error al procesar la resonancia: {str(e)}")
            return self.render_to_response(self.get_context_data())
    