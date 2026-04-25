from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistroForm(UserCreationForm):
    # Definimos el email explícitamente con estilo Bootstrap
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
    )

    class Meta(UserCreationForm.Meta): # type: ignore
        model = CustomUser
        # Solo pedimos 2 campos. Las 2 contraseñas vienen incluidas en el UserCreationForm 
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Este bucle le pone la clase 'form-control' a todos los campos (incluyendo las claves)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'