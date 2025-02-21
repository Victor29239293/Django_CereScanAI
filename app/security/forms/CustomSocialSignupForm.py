from django import forms
from allauth.socialaccount.forms import SignupForm
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()
class CustomSocialSignupform(SignupForm):
    first_name = forms.CharField(
        max_length=30, 
        label='Nombres',
        label_suffix=':',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input form-control', 
            'placeholder': 'Ingrese sus nombres'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        label='Apellidos',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input form-control', 
            'placeholder': 'Ingrese sus apellidos'
        })
    )
    username = forms.CharField(
        max_length=30, 
        label='Nombre de usuario',
        required=True,
        widget=forms.TextInput(attrs={
            'class': ' input form-control', 
            'placeholder': 'Ingrese un nombre de usuario'
        })
    )
    dni = forms.CharField(
        max_length=13, 
        label='Cédula o RUC',
        validators=[
            RegexValidator(
                regex=r'^\d{10,13}$',
                message='Ingrese un número de cédula o RUC válido'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ingrese su cédula o RUC'
        })
    )
    direction = forms.CharField(
        max_length=200, 
        label='Dirección',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ingrese su dirección'
        })
    )
    phone = forms.CharField(
        max_length=50, 
        label='Teléfono',
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Ingrese un número de teléfono válido'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Ingrese su número de teléfono'
        })
    )
    birth_date = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control'
        }),
        required=False
    )
    image = forms.ImageField(
        label='Foto de perfil',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file'
        })
    )

    def save(self, request):
        user = super(CustomSocialSignupform, self).save(request)
        
      
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.dni = self.cleaned_data['dni']
        user.direction = self.cleaned_data['direction']
        user.phone = self.cleaned_data['phone']
        user.birth_date = self.cleaned_data['birth_date']
        user.image = self.cleaned_data['image']
        
        user.save()
        return user

    def clean_dni(self):
        dni = self.cleaned_data['dni']

     
        if len(dni) not in (10, 13):
            raise forms.ValidationError('El número de documento debe tener 10 dígitos para cédula o 13 para RUC')

        if User.objects.filter(dni=dni).exists():
            raise forms.ValidationError('El número de cédula o RUC ya está registrado.')

        return dni
