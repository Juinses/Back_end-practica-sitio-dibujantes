from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.galeria_inicio, name='galeria'),
    
    # Rutas de Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='galeria'), name='logout'),
    path('registro/', views.registro_usuario, name='registro'),
    path('solicitar/<int:obra_id>/', views.solicitar_comision, name='solicitar_comision'),
    path('mis-comisiones/', views.panel_comisiones, name='panel_comisiones'),
    path('cambiar-estado/<int:comision_id>/<str:nuevo_estado>/', views.cambiar_estado_comision, name='cambiar_estado'),
    path('subir-obra/', views.subir_obra, name='subir_obra'),
    path('artistas/', views.lista_artistas, name='lista_artistas'),
    path('artista/<str:nombre_usuario>/', views.perfil_artista, name='perfil_artista'),
    path('mi-perfil/editar/', views.editar_perfil, name='editar_perfil'),
]