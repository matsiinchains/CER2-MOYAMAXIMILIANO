from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# REQ06: Modelo para datos personales adicionales del ciudadano
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)
    instance.perfil.save()

# Modelo para los materiales según ANEXO 2
class Material(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# REQ07 & REQ08: Modelo para las solicitudes de retiro
class SolicitudRetiro(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_RUTA', 'En Ruta'),
        ('COMPLETADA', 'Completada'),
    ]

    ciudadano = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes')
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    cantidad_kg = models.DecimalField(max_digits=5, decimal_places=2, help_text="Cantidad estimada en Kilogramos (Kg)")
    fecha_estimada_retiro = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    
    # REQ09 & REQ10: Campos para la gestión de operarios y staff
    operario_asignado = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='retiros_asignados',
        limit_choices_to={'is_staff': True, 'is_superuser': False}
    )
    comentarios_operario = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Solicitud #{self.pk} de {self.ciudadano.first_name}"