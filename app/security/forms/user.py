from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.security.models import User
from django.forms import ImageField, FileInput
from django import forms
class CustomUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', "birth_date",   'last_name', 'email', 'dni', 'password1', 'password2', 'direction', 'phone', 'image')

class CustomUserUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
    }))

    class Meta:
        model = User  
        fields = [
            "username",  
            "first_name", 
            "last_name", 
            "dni", 
            "phone",  
            "image", 
            "birth_date",  
            "direction"
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'})
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Ingrese nombre de usuario",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "first_name": forms.TextInput(attrs={
                "placeholder": "Ingrese nombres del usuario",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Ingrese apellidos del usuario",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "dni": forms.TextInput(attrs={
                "placeholder": "Ingrese DNI del usuario",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "Ingrese número celular del usuario",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }),
            "birth_date": forms.DateInput(attrs={
                "type": "date",  
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }, format='%Y-%m-%d'),
            "direction": forms.TextInput(attrs={
                "placeholder": "Ingrese dirección del usuario",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            })
        }
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombres",
            "last_name": "Apellidos",
            "dni": "DNI o RUC",
            "phone": "Celular",
            "image": "Imagen",
            "birth_date": "Fecha de nacimiento",
            "direction": "Dirección",
        }
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
       
    if self.instance.birth_date:
        self.fields['birth_date'].initial = self.instance.birth_date.strftime('%Y-%m-%d')