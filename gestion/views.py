from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from .forms import FormularioRegistroUsuario, FormularioSolicitud
from .models import Material, SolicitudRetiro

# REQ03 & REQ04: Vista pública con información y métricas
def home(request):
    materiales = Material.objects.all()
    solicitudes_por_mes = SolicitudRetiro.objects.annotate(mes=TruncMonth('fecha_creacion')).values('mes').annotate(total=Count('id')).order_by('mes')
    materiales_populares = SolicitudRetiro.objects.filter(estado='COMPLETADA').values('material__nombre').annotate(total_kg=Sum('cantidad_kg')).order_by('-total_kg')[:5]
    
    context = {
        'materiales': materiales,
        'solicitudes_por_mes': solicitudes_por_mes,
        'materiales_populares': materiales_populares
    }
    return render(request, 'home.html', context)

# REQ06: Vista para el registro de ciudadanos
def registro(request):
    if request.method == 'POST':
        form = FormularioRegistroUsuario(request.POST)
        if form.is_valid():
            user = form.save()
            user.perfil.telefono = form.cleaned_data.get('telefono')
            user.perfil.direccion = form.cleaned_data.get('direccion')
            user.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Has iniciado sesión.')
            return redirect('dashboard')
    else:
        form = FormularioRegistroUsuario()
    return render(request, 'registration/register.html', {'form': form})

# REQ08: Panel del ciudadano con historial de solicitudes
@login_required
def dashboard(request):
    solicitudes = SolicitudRetiro.objects.filter(ciudadano=request.user)
    return render(request, 'dashboard.html', {'solicitudes': solicitudes})

# REQ07: Vista para crear una nueva solicitud
@login_required
def crear_solicitud(request):
    if request.method == 'POST':
        form = FormularioSolicitud(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.ciudadano = request.user
            solicitud.save()
            messages.success(request, 'Tu solicitud de retiro ha sido creada con éxito.')
            return redirect('dashboard')
    else:
        form = FormularioSolicitud()
    return render(request, 'crear_solicitud.html', {'form': form})