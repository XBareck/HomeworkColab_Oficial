from django.db import models
from django.conf import settings
from trabajos.models import Trabajo
from comentarios.models import Comentario

class Reporte(models.Model):
    TIPOS_REPORTE = [
        ('COPYRIGHT', 'Derechos de Autor'),
        ('SPAM', 'Spam o Publicidad'),
        ('CONTENIDO', 'Contenido Inadecuado'),
        ('ERROR', 'Archivo Corrupto/Error'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_REPORTE)
    razon = models.TextField()
    
    # El reporte puede ser a un trabajo O a un comentario (uno de los dos será null)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, null=True, blank=True)
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, null=True, blank=True)
    
    fecha = models.DateTimeField(auto_now_add=True)
    resuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"Reporte {self.tipo} por {self.usuario.username}"