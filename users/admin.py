from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Perfil

# Registro el Perfil 
admin.site.register(Perfil)

# panel de Django que agrega nuestra nueva casilla
class CustomUserAdmin(UserAdmin):
    fieldsets = (*UserAdmin.fieldsets, (
        'Permisos de HomeworkColab', {'fields': ('is_moderador',)}
    ))

# Registramos el modelo con esta nueva configuración
admin.site.register(CustomUser, CustomUserAdmin)