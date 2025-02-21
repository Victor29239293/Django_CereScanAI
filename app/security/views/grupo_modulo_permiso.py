from django.urls import reverse_lazy
from app.security.forms.grupos_modulos_permisos import GroupModulePermissionForm
from app.security.models import GroupModulePermission
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.db.models import Q
from app.security.instance.menu_module import MenuModule
from django.contrib.auth.decorators import login_required

class GroupModulePermisionsListView(ListView):
    model = GroupModulePermission
    template_name = 'security/auth/seguridad/grupo_modulo_permiso/list.html'
    context_object_name = 'GroupModulePermissions'
    paginate_by=5
    def get_queryset(self):
        
        return super().get_queryset().order_by('id')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)
        return context

class GroupModulePermisionsCreateView(CreateView):
    model = GroupModulePermission
    template_name = 'security/auth/seguridad/grupo_modulo_permiso/form.html'
    form_class = GroupModulePermissionForm
    success_url = reverse_lazy('security:grupo_modulo_permiso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)  
        return context

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error en el campo {field}: {error}")
        return super().form_invalid(form)


class GroupModulePermisionsUpdateView(UpdateView):
    model = GroupModulePermission
    template_name = 'security/auth/seguridad/grupo_modulo_permiso/form.html' 
    fields = ["group", "module", 'permissions']  
    success_url = reverse_lazy('security:grupo_modulo_permiso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context) 
        return context

class GroupModulePermisionsDeleteView(DeleteView):
    model = GroupModulePermission
    template_name = 'security/auth/seguridad/grupo_modulo_permiso/delete.html'
    success_url = reverse_lazy('security:grupo_modulo_permiso')
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)  
        return context