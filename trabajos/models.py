from django.db import models
from django.conf import settings

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Categoría")

    def __str__(self):
        return self.nombre

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Trabajo(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo_url = models.FileField(upload_to='trabajos_academicos/') 
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    # Relaciones
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trabajos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='trabajos')
    etiquetas = models.ManyToManyField(Etiqueta, related_name='trabajos', blank=True)
    
    # Campo para los likes de los trabajos, se relaciona con el modelo de usuario para saber quién le dio like a cada trabajo
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='trabajos_likeados', blank=True)

    def __str__(self):
        return self.titulo
    
    def total_likes(self):
        return self.likes.count()

