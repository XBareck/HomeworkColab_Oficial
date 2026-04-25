from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm 
from trabajos.models import Trabajo

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'users/registro.html', {'form': form})

@login_required
def perfil(request):
    # Filtramos los trabajos: solo los que pertenecen al usuario logueado
    mis_trabajos = Trabajo.objects.filter(usuario=request.user).order_by('-fecha_subida')
    
    return render(request, 'users/perfil.html', {
        'mis_trabajos': mis_trabajos
    })