from django import forms
from django.forms import ModelForm
from app.security.models import Menu

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = [
            "name",
            "icon",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre",
                    "id": "id_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "icon": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el icono",
                    "id": "id_icon",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
        }
        labels = {
            "name": "Nombre",
            "icon": "Icono",
        }
