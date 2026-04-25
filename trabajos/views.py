from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from trabajos.models import Categoria, Trabajo
from .forms import TrabajoForm, ComentarioForm
from comentarios.models import Comentario
from django.contrib import messages as dj_messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

def detalle_trabajo(request, trabajo_id):
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
                # 2. USAMOS EL ALIAS AQUÍ
                dj_messages.success(request, "¡Tu comentario ha sido publicado!")
                return redirect('detalle_trabajo', trabajo_id=trabajo.id)
        else:
            # 3. Y USAMOS EL ALIAS AQUÍ
            dj_messages.error(request, "Debes iniciar sesión para comentar.")

    context = {
        'trabajo': trabajo
    }
    return render(request, 'trabajos/detalle.html', context)

@login_required
def subir_trabajo(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        categoria_id = request.POST.get('categoria')
        archivo = request.FILES.get('archivo_url')

        # Verificación de campos
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
                # Aquí usamos el alias corregido
                dj_messages.error(request, f"Hubo un error al subir el archivo: {e}")

    # Cargar categorías para el GET
    categorias = Categoria.objects.all().order_by('nombre')
    
    # Esto te dirá en la consola si realmente hay datos en la BD
    print(f"DEBUG: Categorías enviadas al HTML: {categorias.count()}")

    return render(request, 'trabajos/subir.html', {'categorias': categorias})

@login_required
def agregar_comentario(request, pk):
    trabajo = get_object_or_404(Trabajo, pk=pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.trabajo = trabajo
            comentario.save()
    return redirect('trabajos:detalle', pk=pk)