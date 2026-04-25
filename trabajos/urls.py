from django.urls import path
from . import views

app_name = 'trabajos' # Espacio de nombres para evitar conflictos

urlpatterns = [
    path('<int:pk>/', views.detalle_trabajo, name='detalle'),
    path('subir/', views.subir_trabajo, name='subir'), 
    path('<int:pk>/comentar/', views.agregar_comentario, name='comentar')
]