from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Perfil

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Perfil)