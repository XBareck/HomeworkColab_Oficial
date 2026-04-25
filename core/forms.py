from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuarioForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): # type: ignore
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') # Campos que quieres pedir
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
        }
        help_texts = {
            'username': 'Letras, números y los caracteres @/./+/-/_ solamente.',
            # Puedes dejar otros en blanco si no quieres los textos de ayuda largos de Django
        }