from django import forms
from app.ScanAI.models import Resonancia, User
import os
import shutil

class ResonanciaForm(forms.ModelForm):
    paciente = forms.ModelChoiceField(
        queryset=User.objects.filter(Paciente__isnull=False),
        empty_label="Seleccione un paciente",
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'required': True
        })
    )
    
    flair = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'accept': '.nii,.nii.gz',
            'required': True
        })
    )
    
    t1ce = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
            'accept': '.nii,.nii.gz',
            'required': True
        })
    )

    class Meta:
        model = Resonancia
        fields = ['paciente', 'flair', 't1ce']

    def clean_flair(self):
        flair = self.cleaned_data.get('flair')
        if flair:
            ext = os.path.splitext(flair.name)[1].lower()
            if ext not in ['.nii', '.nii.gz']:
                raise forms.ValidationError(
                    'El archivo FLAIR debe ser en formato .nii o .nii.gz'
                )
            if flair.size > 100 * 1024 * 1024:
                raise forms.ValidationError(
                    'El archivo FLAIR no puede ser mayor a 100MB'
                )
        return flair

    def clean_t1ce(self):
        t1ce = self.cleaned_data.get('t1ce')
        if t1ce:
            ext = os.path.splitext(t1ce.name)[1].lower()
            if ext not in ['.nii', '.nii.gz']:
                raise forms.ValidationError(
                    'El archivo T1CE debe ser en formato .nii o .nii.gz'
                )
            if t1ce.size > 100 * 1024 * 1024:
                raise forms.ValidationError(
                    'El archivo T1CE no puede ser mayor a 100MB'
                )
        return t1ce

    def save(self, commit=True):
        instance = super().save(commit=False)

 
        flair_temp_path = self.cleaned_data['flair'].temporary_file_path()
        t1ce_temp_path = self.cleaned_data['t1ce'].temporary_file_path()

        if commit:
            instance.save()
            final_flair_path = os.path.join('media/flair', instance.flair.name)
            final_t1ce_path = os.path.join('media/t1ce', instance.t1ce.name)

            shutil.move(flair_temp_path, final_flair_path)
            shutil.move(t1ce_temp_path, final_t1ce_path)

         
            instance.flair.name = final_flair_path
            instance.t1ce.name = final_t1ce_path
            instance.save()  

        return instance
