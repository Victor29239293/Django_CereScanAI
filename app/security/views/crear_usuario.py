from django.urls import reverse_lazy
from django.views.generic import CreateView
from app.security.forms.user import CustomUserCreationForm
from app.security.models import User
from app.security.forms.user import CustomUserCreationForm
from django.contrib import messages
from app.security.instance.menu_module import MenuModule
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.contrib.auth.decorators import login_required

class UserListView(PermissionMixin, ListViewMixin, ListView):
    model = User
    template_name = 'security/auth/seguridad/crear_usuario/list.html'
    context_object_name = 'users'
    paginate_by=4
    def get_queryset(self):
        
        return super().get_queryset().order_by('id')  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)  
        print(context)
        return context

class UserCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = User
    template_name = 'security/auth/seguridad/crear_usuario/form.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('security:crear_usuario_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)
        return context
    
    def form_valid(self, form):
  
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Ya existe Usuario con este Email')
            return self.form_invalid(form)

 
        dni = form.cleaned_data.get('dni')
        if User.objects.filter(dni=dni).exists():
            form.add_error('dni', 'Ya existe un usuario con esta cedula')
            return self.form_invalid(form)

     
        password2 = form.cleaned_data.get('password2')
        
  
        if len(password2) < 8:
            form.add_error('password2', 'Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres')
            return self.form_invalid(form)
        
    
        if password2.isdigit():
            form.add_error('password2', 'Esta contraseña es completamente numérica')
            return self.form_invalid(form)
        
    
        common_passwords = ['12345678', '87654321', '11111111', '00000000', 'password', 'qwerty123']
        if password2.lower() in common_passwords:
            form.add_error('password2', 'Esta contraseña es demasiado común')
            return self.form_invalid(form)
        
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error en el campo {field}: {error}")
        return super().form_invalid(form)

class UserUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = User
    template_name = 'security/auth/seguridad/crear_usuario/form.html'  
    fields = ['username', 'first_name', 'last_name','grupo', 'email',  'dni', 'direction', 'phone', 'image']  
    success_url = reverse_lazy('security:crear_usuario_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        print(context)  
        return context

class UserDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = User
    template_name = 'security/auth/seguridad/crear_usuario/delete.html'
    success_url = reverse_lazy('security:crear_usuario_view')
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        MenuModule(self.request).fill(context)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

       
        if self.object == request.user:
            context = self.get_context_data(object=self.object)
            context['error'] = "No puedes eliminar tu propio usuario."
            return self.render_to_response(context)

        return super().post(request, *args, **kwargs)