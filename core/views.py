from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages as dj_messages 
# IMPORTACIONES DE MODELOS
# Ajusta esta línea dependiendo de si tus modelos están en la app 'core' o 'trabajos'
from trabajos.models import Trabajo, Categoria
# Traemos los modelos de esta misma app ('core')
from .models import Comentario, Reporte
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

User = get_user_model()

# Creamos la función que verifica el rol
def es_admin_o_moderador(user):
    # Si no está logueado, lo rechaza
    if not user.is_authenticated:
        return False
    # Si es superadmin O es moderador, lo deja pasar
    if user.is_superuser or user.is_moderador:
        return True
    # Si es un estudiante normal, lanza un error de "Acceso Denegado"
    raise PermissionDenied

# ==========================================
# VISTAS PÚBLICAS Y DE NAVEGACIÓN
# ==========================================

def home(request):
    """Vista principal con buscador y filtros de categoría"""
    query = request.GET.get('q')
    categoria_id = request.GET.get('cat')
    
    # 1. Base: todos los trabajos ordenados del más nuevo al más viejo
    trabajos = Trabajo.objects.all().order_by('-fecha_subida')

    # 2. Filtrar por texto si buscaron algo
    if query:
        trabajos = trabajos.filter(
            Q(titulo__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )

    # 3. Filtrar por categoría si hicieron clic en un botón
    if categoria_id:
        trabajos = trabajos.filter(categoria_id=categoria_id)

    paginator = Paginator(trabajos, 9)
    numero_pagina = request.GET.get('page')
    trabajos = paginator.get_page(numero_pagina)

    context = {
        'trabajos': trabajos,
        'categorias': Categoria.objects.all().order_by('nombre'),
        'query': query,
    }
    return render(request, 'core/home.html', context)

def detalle_trabajo(request, trabajo_id):
    """Muestra el detalle del trabajo y maneja los comentarios"""
    trabajo = get_object_or_404(Trabajo, id=trabajo_id)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            contenido = request.POST.get('contenido')
            if contenido:
                Comentario.objects.create(
                    trabajo=trabajo,
                    usuario=request.user,
                    texto=contenido
                )
                dj_messages.success(request, "¡Tu comentario ha sido publicado!")
                return redirect('detalle_trabajo', trabajo_id=trabajo.id)
        else:
            dj_messages.error(request, "Debes iniciar sesión para comentar.")

    context = {
        'trabajo': trabajo
    }
    return render(request, 'trabajos/detalle.html', context)

# ==========================================
# VISTAS DE USUARIOS LOGUEADOS
# ==========================================

@login_required
def subir_trabajo(request):
    """Lógica para publicar un nuevo aporte"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria')
        archivo = request.FILES.get('archivo_url')

        if not titulo or not categoria_id or not archivo:
            dj_messages.error(request, "Por favor, completa todos los campos y selecciona un archivo.")
        else:
            try:
                categoria_obj = get_object_or_404(Categoria, id=categoria_id)
                Trabajo.objects.create(
                    usuario=request.user,
                    titulo=titulo,
                    descripcion=descripcion,
                    categoria=categoria_obj,
                    archivo_url=archivo
                )
                dj_messages.success(request, f"¡'{titulo}' se ha publicado con éxito!")
                return redirect('home')
            except Exception as e:
                dj_messages.error(request, f"Hubo un error al subir el archivo: {e}")

    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'trabajos/subir.html', {'categorias': categorias})

# ==========================================
# VISTAS DE ADMINISTRACIÓN (DASHBOARD)
# ==========================================

@user_passes_test(es_admin_o_moderador)
def admin_dashboard(request):
    """Panel de control principal para los administradores"""
    # Protección total: Si no es admin, lo echamos de aquí
    if not request.user.is_staff:
        dj_messages.error(request, "Acceso denegado. Esta área es exclusiva para administradores.")
        return redirect('home')

    # 1. Lista mágica para las tarjetas superiores
    stats_list = [
        ('Usuarios', User.objects.count(), 'primary', 'people-fill'),
        ('Trabajos', Trabajo.objects.count(), 'success', 'file-earmark-text-fill'),
        ('Categorías', Categoria.objects.count(), 'info', 'tags-fill'),
        ('Comentarios', Comentario.objects.count(), 'secondary', 'chat-left-dots-fill'),
    ]

    # 2. Obtener datos clave para el HTML
    reportes_pendientes = Reporte.objects.filter(resuelto=False).order_by('-fecha')
    ultimos_trabajos = Trabajo.objects.all().order_by('-fecha_subida')[:5]
    ultimos_usuarios = User.objects.all().order_by('-date_joined')[:5]
    ultimos_comentarios = Comentario.objects.all().order_by('-fecha')[:10]

    context = {
        'stats_list': stats_list,
        'reportes_pendientes': reportes_pendientes,
        'ultimos_trabajos': ultimos_trabajos,
        'ultimos_usuarios': ultimos_usuarios,
        'ultimos_comentarios': ultimos_comentarios,
    }
    return render(request, 'core/dashboard.html', context)

# ==========================================
# FUNCIONES DE ACCIÓN DEL DASHBOARD (ELIMINAR/RESOLVER)
# ==========================================

@user_passes_test(es_admin_o_moderador)
def resolver_reporte(request, reporte_id):
    """Marca un reporte como falsa alarma (No elimina nada)"""
    if request.method == 'POST' and request.user.is_staff:
        reporte = get_object_or_404(Reporte, id=reporte_id)
        reporte.resuelto = True
        reporte.save()
        dj_messages.success(request, "El reporte fue marcado como resuelto.")
    return redirect('dashboard')

@user_passes_test(es_admin_o_moderador)
def eliminar_trabajo_admin(request, trabajo_id):
    """El martillo de baneo: Elimina el trabajo y todo lo asociado a él"""
    if request.method == 'POST' and request.user.is_staff:
        trabajo = get_object_or_404(Trabajo, id=trabajo_id)
        titulo_borrado = trabajo.titulo
        trabajo.delete()
        dj_messages.success(request, f"¡El trabajo '{titulo_borrado}' ha sido eliminado para siempre!")
    return redirect('dashboard')

@user_passes_test(es_admin_o_moderador)
def eliminar_comentario_admin(request, comentario_id):
    """Borra comentarios tóxicos o spam"""
    if request.method == 'POST' and request.user.is_staff:
        comentario = get_object_or_404(Comentario, id=comentario_id)
        comentario.delete()
        dj_messages.success(request, "Comentario borrado exitosamente.")
    return redirect('dashboard')

@login_required
def reportar(request, tipo_obj, obj_id):
    """Procesa los reportes de los usuarios (tanto para trabajos como comentarios)"""
    if request.method == 'POST':
        tipo_motivo = request.POST.get('tipo_motivo')
        razon = request.POST.get('razon')

        # Variables para saber qué están reportando
        trabajo_reportado = None
        comentario_reportado = None

        # Verificamos si es un trabajo o un comentario
        if tipo_obj == 'trabajo':
            trabajo_reportado = get_object_or_404(Trabajo, id=obj_id)
        elif tipo_obj == 'comentario':
            comentario_reportado = get_object_or_404(Comentario, id=obj_id)

        # Creamos el reporte en la base de datos
        Reporte.objects.create(
            usuario=request.user,
            trabajo=trabajo_reportado,
            comentario=comentario_reportado,
            tipo=tipo_motivo,
            razon=razon
        )

        dj_messages.success(request, "Tu reporte ha sido enviado. ¡Gracias por mantener limpia la comunidad!")

        # Redirigimos al usuario exactamente a la misma página donde estaba
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    # Si alguien intenta entrar a la URL directamente sin enviar el formulario, lo mandamos al home
    return redirect('home')

@user_passes_test(es_admin_o_moderador)
def gestionar_usuarios(request):
    """Página para ver y buscar a todos los usuarios registrados"""
    if not request.user.is_staff:
        dj_messages.error(request, "Acceso denegado.")
        return redirect('home')

    User = get_user_model() # Usamos tu CustomUser
    query = request.GET.get('q')
    
    # Obtenemos todos los usuarios del más nuevo al más antiguo
    usuarios = User.objects.all().order_by('-date_joined')

    # Si el admin buscó un nombre, filtramos la lista
    if query:
        usuarios = usuarios.filter(username__icontains=query)

    context = {
        'usuarios': usuarios,
        'query': query
    }
    return render(request, 'core/gestionar_usuarios.html', context)