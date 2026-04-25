from django.db import models
from django.conf import settings
from trabajos.models import Trabajo

class Comentario(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.trabajo.titulo}"