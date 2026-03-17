from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import PostArte, Perfil
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import ComisionForm, PostArteForm, PerfilForm
from .models import PostArte, Perfil, Comision
from django.contrib.auth.models import User

def galeria_inicio(request):
    # Traemos todas las obras ordenadas por la más reciente
    obras = PostArte.objects.all().order_by('-fecha_publicacion')
    
    # Le pasamos las obras al template a través de un diccionario
    contexto = {
        'obras': obras
    }
    return render(request, 'core/galeria.html', contexto)

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Creamos el perfil automáticamente al registrarse
            Perfil.objects.create(usuario=usuario)
            messages.success(request, f'¡Cuenta creada para {usuario.username}! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    contexto = {'form': form}
    return render(request, 'core/registro.html', contexto)

@login_required
def solicitar_comision(request, obra_id):
    # Buscamos la obra específica en la que el usuario hizo clic
    obra = get_object_or_404(PostArte, id=obra_id)
    artista_perfil = obra.artista
    
    # Validamos que un artista no se pida una comisión a sí mismo
    if request.user == artista_perfil.usuario:
        messages.warning(request, "No puedes solicitarte una comisión a ti mismo.")
        return redirect('galeria')

    if request.method == 'POST':
        form = ComisionForm(request.POST)
        if form.is_valid():
            # commit=False guarda los datos en memoria sin enviarlos a la base de datos aún
            comision = form.save(commit=False)
            # Rellenamos los campos que faltan automáticamente
            comision.cliente = request.user
            comision.artista = artista_perfil
            comision.save() # Ahora sí guardamos
            
            messages.success(request, f"¡Tu solicitud fue enviada a {artista_perfil.usuario.username} con éxito!")
            return redirect('galeria')
    else:
        form = ComisionForm()
    
    contexto = {
        'form': form,
        'obra': obra
    }
    return render(request, 'core/solicitar_comision.html', contexto)

@login_required
def panel_comisiones(request):
    # Usamos hasattr para comprobar si el usuario tiene un perfil sin que el código explote
    es_artista = hasattr(request.user, 'perfil') and request.user.perfil.es_artista
    
    if es_artista:
        # Solo buscamos recibidas si realmente es un artista
        recibidas = Comision.objects.filter(artista=request.user.perfil).order_by('-fecha_solicitud')
    else:
        recibidas = []
        
    pedidas = Comision.objects.filter(cliente=request.user).order_by('-fecha_solicitud')
    
    contexto = {
        'comisiones_recibidas': recibidas,
        'comisiones_pedidas': pedidas,
        'es_artista': es_artista, # Le pasamos esta variable al HTML
    }
    return render(request, 'core/panel_comisiones.html', contexto)

@login_required
def cambiar_estado_comision(request, comision_id, nuevo_estado):
    comision = get_object_or_404(Comision, id=comision_id)
    
    # SEGURIDAD: Verificamos que solo el artista dueño de la comisión pueda cambiar su estado
    if request.user == comision.artista.usuario:
        comision.estado = nuevo_estado
        comision.save()
        messages.success(request, f"Estado actualizado a: {comision.get_estado_display()}")
    else:
        messages.error(request, "No tienes permiso para modificar esta comisión.")
        
    return redirect('panel_comisiones')

@login_required
def subir_obra(request):
    # Bloqueamos el paso a los que no son artistas
    if not hasattr(request.user, 'perfil') or not request.user.perfil.es_artista:
        messages.error(request, "Solo los artistas registrados pueden subir obras.")
        return redirect('galeria')

    if request.method == 'POST':
        # IMPORTANTE: request.FILES es vital para procesar imágenes en Django
        form = PostArteForm(request.POST, request.FILES) 
        if form.is_valid():
            obra = form.save(commit=False)
            obra.artista = request.user.perfil
            obra.save()
            messages.success(request, "¡Tu obra fue publicada con éxito!")
            return redirect('galeria')
    else:
        form = PostArteForm()
        
    return render(request, 'core/subir_obra.html', {'form': form})

def lista_artistas(request):
    # Buscamos solo los perfiles que son de artistas
    artistas = Perfil.objects.filter(es_artista=True)
    
    contexto = {
        'artistas': artistas
    }
    return render(request, 'core/lista_artistas.html', contexto)

def perfil_artista(request, nombre_usuario):
    # Buscamos al usuario por el nombre que viene en la URL
    usuario = get_object_or_404(User, username=nombre_usuario)
    
    # Buscamos su perfil y nos aseguramos de que realmente sea un artista
    perfil = get_object_or_404(Perfil, usuario=usuario, es_artista=True)
    
    # Traemos solo las obras de este artista específico
    obras = PostArte.objects.filter(artista=perfil).order_by('-fecha_publicacion')
    
    contexto = {
        'artista': perfil,
        'obras': obras
    }
    return render(request, 'core/perfil_artista.html', contexto)

@login_required
def editar_perfil(request):
    # Obtenemos el perfil del usuario actual
    perfil = request.user.perfil
    
    if request.method == 'POST':
        # Le pasamos los datos del form, los archivos (foto) y le decimos qué perfil actualizar (instance=perfil)
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu perfil ha sido actualizado!")
            # Si es artista, lo mandamos a ver cómo quedó su página pública
            if perfil.es_artista:
                return redirect('perfil_artista', nombre_usuario=request.user.username)
            return redirect('galeria') # Si es cliente, lo mandamos al inicio
    else:
        # Si entra por primera vez, le mostramos el formulario con sus datos actuales
        form = PerfilForm(instance=perfil)
        
    return render(request, 'core/editar_perfil.html', {'form': form})