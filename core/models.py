from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    es_artista = models.BooleanField(default=False)
    biografia = models.TextField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    
    def __str__(self):
        return self.usuario.username

class PostArte(models.Model):
    artista = models.ForeignKey(Perfil, on_delete=models.CASCADE, limit_choices_to={'es_artista': True})
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='obras/')
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} por {self.artista.usuario.username}"

class Comision(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('rechazada', 'Rechazada'),
    ]
    
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comisiones_solicitadas')
    artista = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='comisiones_recibidas')
    detalles_solicitud = models.TextField(help_text="Describe lo que quieres que el artista dibuje/cree.")
    precio_ofrecido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comisión de {self.cliente.username} para {self.artista.usuario.username}"