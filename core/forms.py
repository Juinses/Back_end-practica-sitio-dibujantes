from django import forms
from django.core.exceptions import ValidationError  
from .models import Comision, PostArte, Perfil

class ComisionForm(forms.ModelForm):
    class Meta:
        model = Comision
        fields = ['detalles_solicitud', 'precio_ofrecido']
        
        widgets = {
            'detalles_solicitud': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Ej: Me gustaría un retrato de mi personaje estilo anime...'
            }),
            'precio_ofrecido': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: 15000',
                'min': '0'  # <-- Validación Front-End (HTML5)
            })
        }
        labels = {
            'detalles_solicitud': '¿Qué deseas que el artista dibuje?',
            'precio_ofrecido': 'Tu oferta de precio (CLP)'
        }

    # Validación Back-End (Python)
    def clean_precio_ofrecido(self):
        precio = self.cleaned_data.get('precio_ofrecido')
        
        # Verificamos que se haya ingresado un precio y que no sea menor a 0
        if precio is not None and precio < 0:
            raise ValidationError("El precio no puede ser negativo. ¡El arte cuesta plata!")
            
        return precio

class PostArteForm(forms.ModelForm):
    class Meta:
        model = PostArte
        fields = ['titulo', 'imagen', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de tu obra'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil', 'biografia']
        widgets = {
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cuéntale a la comunidad sobre ti y tu arte...'}),
        }
        labels = {
            'foto_perfil': 'Foto de Perfil',
            'biografia': 'Tu Biografía'
        }