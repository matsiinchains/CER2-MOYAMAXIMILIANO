from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario, Material, SolicitudRetiro

class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False

class CustomUserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(SolicitudRetiro)
class SolicitudRetiroAdmin(admin.ModelAdmin):
    list_display = ('id', 'ciudadano', 'material', 'estado', 'operario_asignado', 'fecha_estimada_retiro')
    list_filter = ('estado', 'material', 'operario_asignado')
    search_fields = ('id', 'ciudadano__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs 
        return qs.filter(operario_asignado=request.user)

   
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser: 
            return (
                ('Detalles de la Solicitud', {'fields': ('ciudadano', 'material', 'cantidad_kg', 'fecha_estimada_retiro')}),
                ('Gestión (Staff)', {'fields': ('estado', 'operario_asignado', 'comentarios_operario')})
            )
        else: 
            return (
                ('Detalles de la Solicitud Asignada', {'fields': ('ciudadano', 'material', 'cantidad_kg', 'fecha_estimada_retiro')}),
                ('Actualización (Operario)', {'fields': ('estado', 'comentarios_operario')})
            )
            
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('ciudadano', 'material', 'cantidad_kg', 'fecha_estimada_retiro', 'operario_asignado')
        return ('ciudadano',)

    def get_list_editable(self, request):
        if request.user.is_superuser: 
            return ('estado', 'operario_asignado')
        return ('estado',) 
