from django import forms
from django.forms import ModelForm
from app.security.models import GroupModulePermission, Module

class GroupModulePermissionForm(ModelForm):
    class Meta:
        model = GroupModulePermission
        fields = [
            "group",
            "module",
            "permissions",
        ]
        widgets = {
            "group": forms.Select(
                attrs={
                    "id": "id_group",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "module": forms.Select(
                attrs={
                    "id": "id_module",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "onchange": "fetch_permissions(this.value)",
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
            "group": "Grupo",
            "module": "Módulo",
            "permissions": "Permisos",
        }
