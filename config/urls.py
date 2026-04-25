from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views as core_views

from trabajos import views # Importamos las vistas de autenticación

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('trabajos/', include('trabajos.urls')),
    # Esta línea registra automáticamente login y logout
    path('usuarios/', include('users.urls')), # Verifica que no tenga un namespace aquí
    path('accounts/', include('django.contrib.auth.urls')), # Para login/logout 
    path('dashboard/', core_views.admin_dashboard, name='dashboard'),
    path('trabajo/<int:trabajo_id>/', views.detalle_trabajo, name='detalle_trabajo'),
]


# Esto es vital para que las imágenes y PDFs se puedan ver/descargar en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)