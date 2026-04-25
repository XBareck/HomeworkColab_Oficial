from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # RUTAS PÚBLICAS Y PRINCIPALES
    # ==========================================
    path('', views.home, name='home'),
    
    # Ruta para que los usuarios puedan reportar cosas
    path('reportar/<str:tipo_obj>/<int:obj_id>/', views.reportar, name='reportar'),  # type: ignore

    # ==========================================
    # PANEL DE ADMINISTRACIÓN (DASHBOARD)
    # ==========================================
    # Nota: El name es 'dashboard' para que los botones de la Navbar funcionen
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('dashboard/usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),

    # ==========================================
    # ACCIONES DEL DASHBOARD (ELIMINAR/RESOLVER)
    # ==========================================
    # Rutas exactas que coinciden con los botones de eliminar y nuestro views.py
    path('dashboard/reporte/<int:reporte_id>/resolver/', views.resolver_reporte, name='resolver_reporte'),
    path('dashboard/trabajo/<int:trabajo_id>/eliminar/', views.eliminar_trabajo_admin, name='eliminar_trabajo_admin'),
    path('dashboard/comentario/<int:comentario_id>/eliminar/', views.eliminar_comentario_admin, name='eliminar_comentario_admin'),
]