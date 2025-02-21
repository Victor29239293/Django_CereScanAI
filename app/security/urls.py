# myapp/urls.py
from django.urls import path, include
from app.security.views.auth import SignupView, SigninView, logout_view, perfil_usuario, editar_perfil,CustomConnectionsView, desvincular_cuenta
from app.security.views import modulos,menu,grupo_modulo_permiso,crear_usuario
from app.security.views.menu import MenuCreateView,MenuUpdateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'security' 

urlpatterns = [
    path('custom-register/', SignupView.as_view(), name='custom_register'),
    path('custom-login/', SigninView.as_view(), name='custom_login'),
    path('logout/', logout_view, name='logout'),

    path("perfil/", perfil_usuario, name="perfil"),
    path("editar_perfil/", editar_perfil, name="editar_perfil"),
    # path("accounts/3rdparty/signup/", signupGoogle, name="signup"),
    
    path(
        'accounts/social/connections/', 
        CustomConnectionsView.as_view(), 
        name='socialaccount_connections'
    ),
    
    # URL opcional para desvinculación
    path(
        'desvincular-cuenta/',
        desvincular_cuenta,
        name='desvincular_cuenta'
    ),
    
      # URLs de recuperación de contraseña
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='security/auth/password_reset_form.html',
             email_template_name='security/auth/password_reset_email.html',
             subject_template_name='security/auth/password_reset_subject.txt',
             success_url=reverse_lazy('security:password_reset_done')
         ), 
         name='password_reset'),



    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='security/auth/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='security/auth/password_reset_confirm.html',
             success_url=reverse_lazy('security:password_reset_complete')
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='security/auth/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    
    
        
    # path('modulo_view/', modulos.ModuleListView.as_view(), name='module_view'),
    path('modulo_view/nuevo/', modulos.ModuleCreateView.as_view(), name='modulo_create'),
    path('modulo_view/editar/<int:pk>/', modulos.ModuleUpdateView.as_view(), name='modulo_update'),  # Verifica esta línea
    path('modulo_view/eliminar/<int:pk>/', modulos.ModuleDeleteView.as_view(), name='modulo_delete'),
    path('modulos/', modulos.ModuleListView.as_view(), name='module_list'),
    path('modulos/crear/', modulos.ModuleCreateView.as_view(), name='view'),
    
    path('menu_view/', menu.MenuListView.as_view(), name='menu_view'),
    path('menu_view/nuevo/', menu.MenuCreateView.as_view(), name='menu_create'),
    path('menu_view/editar/<int:pk>/', menu.MenuUpdateView.as_view(), name='menu_update'),  # Verifica esta línea
    path('menu_view/eliminar/<int:pk>/', menu.MenuDeleteView.as_view(), name='menu_delete'),
    
    path('grupo_modulo_permiso/', grupo_modulo_permiso.GroupModulePermisionsListView.as_view(), name='grupo_modulo_permiso'),
    path('grupo_modulo_permiso/nuevo/', grupo_modulo_permiso.GroupModulePermisionsCreateView.as_view(), name='grupo_modulo_permiso_create'),
    path('grupo_modulo_permiso/editar/<int:pk>/', grupo_modulo_permiso.GroupModulePermisionsUpdateView.as_view(), name='grupo_modulo_permiso_update'),  # Verifica esta línea
    path('grupo_modulo_permiso/eliminar/<int:pk>/', grupo_modulo_permiso.GroupModulePermisionsDeleteView.as_view(), name='grupo_modulo_permiso_delete'),
    path('grupo_modulo_permiso/', grupo_modulo_permiso.GroupModulePermisionsListView.as_view(), name='grupo_modulo_permiso_list'),
    
    path('grupo_modulo_permiso/crear/', grupo_modulo_permiso.GroupModulePermisionsCreateView.as_view(), name='view'),
    path('crear_usuario/', crear_usuario.UserListView.as_view(), name='crear_usuario_view'),
    path('crear_usuario/nuevo/', crear_usuario.UserCreateView.as_view(), name='crear_usuario_create'),
    path('crear_usuario/editar/<int:pk>/', crear_usuario.UserUpdateView.as_view(), name='crear_usuario_update'),  # Verifica esta línea
    path('crear_usuario/eliminar/<int:pk>/', crear_usuario.UserDeleteView.as_view(), name='crear_usuario_delete'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
