from django.shortcuts import render, redirect, get_object_or_404
from app.security.models import Module  # Asegúrate de importar tu modelo Module
from app.security.forms.moduls import ModuleForm  # Asegúrate de que tu formulario está bien importado
from app.security.instance.menu_module import MenuModule
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.security.forms.menu import MenuForm  # Asegúrate de tener esta importación correcta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
class ModuleListView(ListView):
    model = Module
    template_name = 'security/auth/seguridad/module/list.html'
    context_object_name = 'modulos'
    paginate_by=5
    def get_queryset(self):
        
        return super().get_queryset().order_by('id')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)
        return context

class ModuleCreateView(CreateView):
    model = Module
    template_name = 'security/auth/seguridad/module/form.html'
    form_class = ModuleForm
    success_url = reverse_lazy('security:module_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)  # Debug para verificar el contexto
        return context
    
    def form_valid(self, form):
        url = form.cleaned_data.get('url')
        if Module.objects.filter(url=url).exists():
            messages.error(self.request, f"No se pudo guardar el módulo. Ya existe un módulo con la URL '{url}'.")
            return self.form_invalid(form)
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error en el campo {field}: {error}")
        return super().form_invalid(form)


class ModuleUpdateView(UpdateView):
    model = Module
    template_name = 'security/auth/seguridad/module/form.html'  # Asegúrate de que la ruta sea correcta
    fields = ['url', 'name', 'menu', 'description', 'icon', 'is_active', 'permissions']  # Ajusta según tus campos
    success_url = reverse_lazy('security:module_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)  
        return context

class ModuleDeleteView(DeleteView):
    model = Module
    template_name = 'security/auth/seguridad/module/delete.html'
    success_url = reverse_lazy('security:module_list')
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        try:
            self.object.delete()
            messages.success(request, "Módulo eliminado con éxito.")
            return redirect(self.success_url)
        except ProtectedError:
           
            context['error'] = "No se puede eliminar el módulo porque está asociado a uno o más grupos de permisos."
            return self.render_to_response(context)