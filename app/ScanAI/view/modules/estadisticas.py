import json
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import TemplateView
from app.ScanAI.models import Resonancia
from app.security.instance.menu_module import MenuModule
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required


class EstadisticasView(TemplateView):
    template_name = "Dashboard/modules/Estadisticas/views_estadisticas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)


        estadisticas = (
            Resonancia.objects
            .annotate(fecha_truncada=TruncDate("fecha"))  
            .values("fecha_truncada", "tipo_anomalia")
            .annotate(count=Count("id"))
            .order_by("fecha_truncada")
        )

  
        estadisticas_anomalias = [
            {"fecha": item["fecha_truncada"].strftime("%Y-%m-%d"), "tipo_anomalia": item["tipo_anomalia"], "count": item["count"]}
            for item in estadisticas
        ]

      
        print("Datos de estadísticas:", estadisticas_anomalias)

        context['estadisticas_anomalias'] = json.dumps(estadisticas_anomalias, cls=DjangoJSONEncoder)
        return context
