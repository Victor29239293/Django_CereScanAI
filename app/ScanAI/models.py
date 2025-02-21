from django.db import models
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Paciente')
    historial_medico = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} - Paciente"

    @property
    def edad(self):
        if self.user.birth_date:
            today = date.today()
            age = today.year - self.user.birth_date.year
            if (today.month, today.day) < (self.user.birth_date.month, self.user.birth_date.day):
                age -= 1
            return age
        return None


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Doctor')
    especialidad = models.CharField(max_length=80, verbose_name="Especialidad")

    def __str__(self):
        return f"{self.user.first_name} - Doctor"



class Resonancia(models.Model):
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resonancias')
    flair = models.FileField(upload_to='Resonancias/flair/', blank=True, null=True)
    t1ce = models.FileField(upload_to='Resonancias/t1ce/', blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    informe_ia = models.FileField(upload_to='informes/', blank=True, null=True)
    tipo_anomalia = models.CharField(max_length=200, blank=True, null=True)
    severidad_anomalia = models.CharField(max_length=50, blank=True, null=True)
    recomendacion_medica = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return f"Resonancia de {self.paciente.first_name}"


    def generar_informe(self):
        return f"Informe de Resonancia de {self.paciente.first_name} {self.paciente.last_name}:\n" \
               f"Fecha: {self.fecha}\n" \
               f"Anomalía detectada: {self.tipo_anomalia}\n" \
               f"Severidad: {self.severidad_anomalia}\n" \
               f"Recomendación médica: {self.recomendacion_medica}\n" \
               f"Informe detallado del análisis IA:\n{self.informe_ia}"
               
   

class Informe(models.Model):
    resonancia = models.OneToOneField('Resonancia', on_delete=models.CASCADE, related_name='informe')
    fecha_generacion = models.DateField(auto_now_add=True)
    recomendaciones_adicionales = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Informe de   -"

    @property
    def detalles_informe(self):
        return f"Informe de Resonancia:\n" \
               f"Paciente: {self.resonancia.paciente.get_full_name()}\n" \
               f"Fecha de la resonancia: {self.resonancia.fecha}\n" \
               f"Tipo de anomalía: {self.resonancia.tipo_anomalia or 'N/A'}\n" \
               f"Severidad de la anomalía: {self.resonancia.severidad_anomalia or 'N/A'}\n" \
               f"Recomendación médica: {self.resonancia.recomendacion_medica or 'N/A'}\n" \
               f"Recomendaciones adicionales: {self.recomendaciones_adicionales or 'N/A'}"

    @property
    def imagenes_resonancia(self):
        # Devuelve las URLs de todas las imágenes asociadas a la resonancia
        return [imagen.imagen.url for imagen in self.resonancia.imagenes.all()]

class ResonanciaImagen(models.Model):
    resonancia = models.ForeignKey(Resonancia, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='resultados_ia/')

    def __str__(self):
        return f"{self.resonancia}"


