
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group
from app.ScanAI.models import PatientProfile
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        self._assign_patient_role(user)
        return user

    def _assign_patient_role(self, user):
        try:
            patient_group = Group.objects.get(name="PACIENTE")
            user.groups.add(patient_group)
            
      
            if not PatientProfile.objects.filter(user=user).exists():
                PatientProfile.objects.create(user=user)
        except Group.DoesNotExist:
            pass

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
       
        CustomAccountAdapter()._assign_patient_role(user)
        return user

    def get_connect_redirect_url(self, request, socialaccount):
    
        return reverse('security:perfil_usuario')

    def get_login_redirect_url(self, request):
     
        return reverse('security:perfil_usuario')