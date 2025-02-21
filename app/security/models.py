import json
from crum import get_current_request
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import models
from django.forms import model_to_dict
from django.contrib.auth import get_user_model
from datetime import date
from CereScanAI.utils import valida_cedula , phone_regex

class Menu(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=150, unique=True)
    icon = models.CharField(verbose_name='Icono', max_length=100)
  
    def __str__(self):
        return self.name

    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'bi bi-calendar-x-fill'

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        ordering = ['-name']


class Module(models.Model):
    url = models.CharField(verbose_name='Url', max_length=100, unique=True)
    name = models.CharField(verbose_name='Nombre', max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT,verbose_name='Menu')
    description = models.CharField(
        verbose_name='Descripción',
        max_length=200,
        null=True,
        blank=True
    )
    icon = models.CharField(verbose_name='Icono', max_length=100, null=True,
                            blank=True)
    is_active = models.BooleanField(verbose_name='Es activo', default=True)
    permissions = models.ManyToManyField(
        verbose_name='Permisos',
        to=Permission,
        blank=True
    )

   
    def __str__(self):
        return '{} [{}]'.format(self.name, self.url)

    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    def get_icon(self):
        if self.icon:
            return self.icon
        return 'bi bi-x-octagon'

    class Meta:
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'
        ordering = ('-name',)

class GroupModulePermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.PROTECT,verbose_name='Grupo')
    module = models.ForeignKey(Module, on_delete=models.PROTECT,verbose_name='Modulo')
    permissions = models.ManyToManyField(Permission, blank=True,verbose_name='Permisos')

    def __str__(self):
        return f"{self.module.name} -{self.group.name}"

    @staticmethod

    def get_group_module_permission_active_list(group_id):
        return GroupModulePermission.objects.select_related(
            'module',
            'module__menu'
        ).filter(
            group_id=group_id,
            module__is_active=True
        )

    class Meta:
        verbose_name = 'Grupo modulo permiso'
        verbose_name_plural = 'Grupos modulos Permisos'
        ordering = ('-id',)


class User(AbstractUser):
    dni = models.CharField(verbose_name='Cédula o RUC', max_length=10, unique=True,  blank=True,null=True, validators=[valida_cedula])
    image = models.ImageField(
        verbose_name='Archive image',
        upload_to='users/',
        max_length=1024,
        blank=True,
        null=True
    )
    email = models.EmailField('Email',unique=True)
    direction=models.CharField('Direccion',max_length=200,blank=True,null=True)
    phone=models.CharField('Telefono',max_length=50,blank=True,null=True,validators=[phone_regex])
    birth_date = models.DateField(null=True, blank=True)
    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

        permissions = (
            (
                "change_userprofile",
                f"Cambiar perfil {verbose_name}"
            ),
            (
                "change_userpassword",
                f"Cambiar password {verbose_name}"
            ),
          
        )
    

    @property
    def edad(self):
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year
            if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
                age -= 1
            return age
        return None
    
    def __str__(self):
        return '{}'.format(self.username)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_groups(self):
        return self.groups.all()

    def get_short_name(self):
        return self.username

    def get_group_session(self):
        request = get_current_request()
        print("request==>", request)

        group_id = request.session.get('group_id')
        if group_id is not None:
            return Group.objects.get(pk=group_id)
        else:
            return None 

    def set_group_session(self):
        request = get_current_request()

        if 'group' not in request.session:

            groups = request.user.groups.all().order_by('id')

            if groups.exists():
                request.session['group'] = groups.first()
                request.session['group_id'] = request.session['group'].id
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/static/img/usuario_anonimo.png'
    def is_patient(self):
        return self.groups.filter(name='Paciente').exists()

    def is_doctor(self):
        return self.groups.filter(name='Especialista').exists()

    def get_role(self):
        if self.is_patient():
            return 'Paciente'
        elif self.is_doctor():
            return 'Doctor'
        elif self.is_superuser:
            return 'Administrador'
        else:
            return 'Usuario sin rol específico'

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            if hasattr(self, 'patient_profile'):
                patient_group = Group.objects.get(name='Paciente')
                self.groups.add(patient_group)
            elif hasattr(self, 'doctor_profile'):
                doctor_group = Group.objects.get(name='DOCTOR')
                self.groups.add(doctor_group)

class AuditUser(models.Model):
    TIPOS_ACCIONES = (
        ('A', 'A'),   
        ('M', 'M'),   
        ('E', 'E')    
    )
    usuario = models.ForeignKey(User, verbose_name='Usuario',on_delete=models.PROTECT)
    tabla = models.CharField(max_length=100, verbose_name='Tabla')
    registroid = models.IntegerField(verbose_name='Registro Id')
    accion = models.CharField(choices=TIPOS_ACCIONES, max_length=10, verbose_name='Accion')
    fecha = models.DateField(verbose_name='Fecha')
    hora = models.TimeField(verbose_name='Hora')
    estacion = models.CharField(max_length=100, verbose_name='Estacion')

    def __str__(self):
        return "{} - {} [{}]".format(self.usuario.username, self.tabla, self.accion)

    class Meta:
        verbose_name = 'Auditoria Usuario '
        verbose_name_plural = 'Auditorias Usuarios'
        ordering = ('-fecha', 'hora')