from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Permission
from app.security.models import Module, Menu

class ModuleForm(ModelForm):
    class Meta:
        model = Module
        fields = [
            "url",
            "name",
            "menu",
            "description",
            "icon",
            "is_active",
            "permissions",
        ]
        widgets = {
            "url": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese la URL",
                    "id": "id_url",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese el nombre",
                    "id": "id_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "menu": forms.Select(
                attrs={
                    "id": "id_menu",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "description": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese la descripción",
                    "id": "id_description",
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
            "is_active": forms.CheckboxInput(
                attrs={
                    "id": "id_is_active",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block",
                }
            ),
            "permissions": forms.SelectMultiple(
                attrs={
                    "id": "id_permissions",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
        }
        labels = {
            "url": "URL",
            "name": "Nombre",
            "menu": "Menú",
            "description": "Descripción",
            "icon": "Icono",
            "is_active": "Es activo",
            "permissions": "Permisos",
        }