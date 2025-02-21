from django.urls import reverse_lazy
from app.security.forms.menu import MenuForm
from app.security.models import Menu
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.db.models import Q
from app.security.instance.menu_module import MenuModule
from django.contrib.auth.decorators import login_required


class MenuListView(PermissionMixin, ListViewMixin, ListView):
    model = Menu
    template_name = 'security/auth/seguridad/menu/list.html'
    context_object_name = 'menus'
    paginate_by = 5

    def get_queryset(self):
       
        return super().get_queryset().order_by('id')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)
        return context

    

class MenuCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Menu
    template_name = 'security/auth/seguridad/menu/form.html'
    form_class = MenuForm
    success_url = reverse_lazy('security:menu_view')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)  # Debug para verificar el contexto
        return context
    
    def form_valid(self, form):
        # Si necesitas validar algo único, usa el campo 'name' que sí existe
        name = form.cleaned_data.get('name')
        if Menu.objects.filter(name=name).exists():
            form.add_error('name', 'Ya existe un menú con este nombre')
            return self.form_invalid(form)
        
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error en el campo {field}: {error}")
        return super().form_invalid(form)

class MenuUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Menu
    template_name = 'security/auth/seguridad/menu/form.html'  
    fields = ['name','icon']  
    success_url = reverse_lazy('security:menu_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)  
        return context

class MenuDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Menu
    template_name = 'security/auth/seguridad/menu/delete.html'
    success_url = reverse_lazy('security:menu_view')
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)  
        return context