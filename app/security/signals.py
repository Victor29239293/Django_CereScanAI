from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from app.ScanAI.models import PatientProfile

@receiver(user_signed_up)
def add_user_to_paciente_group(request, user, **kwargs):
    try:
        patient_group = Group.objects.get(name="Paciente")
        user.groups.add(patient_group)
        

        if not PatientProfile.objects.filter(user=user).exists():
            PatientProfile.objects.create(user=user)
    except Group.DoesNotExist:
        print("No existe el grupo 'Paciente'")
