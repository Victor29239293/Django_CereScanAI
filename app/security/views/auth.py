from django.views.generic import FormView, CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout, authenticate  # Renombramos login para evitar conflictos
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from app.security.forms.user import CustomUserCreationForm, CustomUserUpdateForm
from app.ScanAI.models import PatientProfile
from allauth.account.signals import user_signed_up
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.views import ConnectionsView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
import json
User = get_user_model()

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "security/auth/register.html"
    success_url = reverse_lazy("security:perfil")
    permission_required = 'add_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar User'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        try:
            patient_group = Group.objects.get(name="PACIENTE")
            user.groups.add(patient_group)
        except Group.DoesNotExist:
            messages.error(self.request, "El grupo 'Paciente' no existe. Por favor, créalo.")
            return redirect(self.success_url)
        
      
        PatientProfile.objects.create(user=user)
        
      
        backend = 'django.contrib.auth.backends.ModelBackend'  
        user.backend = backend
        auth_login(self.request, user)  #
        print(self.request, f"Cuenta creada exitosamente para {user.email}. Ahora has iniciado sesión.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        email = form.data.get('email') 

        if (User.objects.filter(email=email).exists()): 
            messages.error(self.request, "El email ya se encuentra en uso")

       
        return super().form_invalid(form)

class SigninView(FormView):
    form_class = AuthenticationForm
    template_name = "security/auth/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data.get('username')  
        password = form.cleaned_data.get('password')

    
        user = authenticate(self.request, username=email, password=password)

     
        if user is None:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(self.request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None and user.is_active:
            backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = backend
            auth_login(self.request, user)  
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, "Credenciales incorrectas o cuenta inactiva.")
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('home')


class CustomConnectionsView(LoginRequiredMixin, ConnectionsView):
    template_name = 'socialaccount/connections.html'
    
    def get_context_data(self, **kwargs):
        google_connected = SocialAccount.objects.filter(
            user=self.request.user,
            provider='google'
        ).exists()
        
        social_account = SocialAccount.objects.filter(
            user=self.request.user,
            provider='google'
        ).first()
        
        print("Google connected:", google_connected)
        if social_account:
            print("Social account email:", social_account.extra_data.get('email'))
        
        context = {
            'google_connected': google_connected,
            'social_account': social_account,
            'user': self.request.user
        }
        return context




def desvincular_cuenta(request):
    if request.method == 'POST':
        data = json.loads(request.body) 
        account_id = data.get('account_id')
        print("Account ID recibido:", account_id)  

        if not account_id:
            return JsonResponse({'success': False, 'message': 'No se proporcionó la cuenta a desvincular.'})

        try:
            account = get_object_or_404(SocialAccount, id=account_id, user=request.user)
            email = account.extra_data.get('email', '')
            account.delete()
            return JsonResponse({'success': True, 'message': f'La cuenta de Google ({email}) ha sido desvinculada exitosamente.'})
        except SocialAccount.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No se encontró la cuenta a desvincular.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


def perfil_usuario(request):
    google_connected = SocialAccount.objects.filter(
        user=request.user,
        provider='google'
    ).exists()
    
    social_account = SocialAccount.objects.filter(
        user=request.user,
        provider='google'
    ).first()
    
    print("Google connected:", google_connected)
    if social_account:
        print("Social account email:", social_account.extra_data.get('email'))

    context = {
        'google_connected': google_connected,
        'social_account': social_account,
        'user': request.user
    }
    return render(request, 'Dashboard/perfil.html', context)



def editar_perfil(request): 

    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            print(request, '¡Tu perfil ha sido actualizado exitosamente!')
            return redirect('security:perfil')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    
    return render(request, 'Dashboard/edit_profile.html', {'form': form})



