from django import forms
from .models import Trabajo
from comentarios.models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe una sugerencia o duda académica...'
            }),
        }

class TrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = ['titulo', 'descripcion', 'categoria', 'archivo_url']
        
        # Aplicamos estilos de Bootstrap a los campos
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ensayo sobre la Revolución Industrial'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe brevemente el contenido...'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'archivo_url': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }