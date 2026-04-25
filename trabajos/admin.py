from django.contrib import admin
from .models import Categoria, Etiqueta, Trabajo

admin.site.register(Categoria)
admin.site.register(Etiqueta)
admin.site.register(Trabajo)