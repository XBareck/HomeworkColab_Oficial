from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# MODELO DE USUARIO CREADO PARA EL PROYECTO, HEREDA DE AbstractUser PARA PODER USAR LOS CAMPOS POR DEFECTO DE DJANGO Y AÑADIR LOS QUE NECESITEMOS

class CustomUser(AbstractUser):
    fecha_registro= models.DateTimeField(auto_now_add=True)
     #definir si el usuario es moderador o no, esto se usará para mostrar opciones adicionales en la interfaz de usuario y para controlar el acceso a ciertas funciones de moderación.
    is_moderador = models.BooleanField('Es Moderador', default=False)
    def __str__(self):
        return self.username
    
# El perfil que guarda la foto y detalles adicionales del usuario, se relaciona con el CustomUser mediante una relación uno a uno, lo que significa que cada usuario tiene un perfil único.
class Perfil(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to="perfiles/", blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True)
   

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

# Esta señal asegura que cada vez que alguien se registre, se cree su perfil automáticamente
@receiver(post_save, sender=CustomUser)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)