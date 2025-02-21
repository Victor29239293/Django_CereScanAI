from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import PermissionMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

class DashboardView(PermissionMixin, TemplateView):
    template_name = 'Dashboard/base.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)
        return context

