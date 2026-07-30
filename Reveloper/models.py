from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tareas_completadas = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Proyecto(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activo', 'Activo'),
            ('completado', 'Completado'),
            ('en pausa', 'En Pausa'),
        ],
    )

    def __str__(self):
        return self.nombre


class TareaPorDesarrollar(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
    )
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
    )
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('en progreso', 'En Progreso'),
            ('completada', 'Completada'),
            ('en revision', 'En Revisión'),
        ],
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'


class TareasCompletadas(models.Model):
    tarea_original_id = models.CharField(max_length=100)
    titulo = models.CharField(max_length=255)
    fecha_entrega = models.DateTimeField()
    estado = models.CharField(max_length=50)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
    )
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Tarea Completada'
        verbose_name_plural = 'Tareas Completadas'


@receiver(post_save, sender=TareaPorDesarrollar)
def transfer_to_completadas(sender, instance, **kwargs):
    if instance.estado != 'completada':
        return

    fecha_entrega = instance.fecha_vencimiento

    if not isinstance(fecha_entrega, datetime):
        fecha_entrega = datetime.combine(
            fecha_entrega,
            datetime.min.time(),
        )

    if timezone.is_naive(fecha_entrega):
        fecha_entrega = timezone.make_aware(fecha_entrega)

    _, created = TareasCompletadas.objects.get_or_create(
        tarea_original_id=instance.id,
        defaults={
            'titulo': instance.titulo,
            'fecha_entrega': fecha_entrega,
            'estado': instance.estado,
            'usuario': instance.usuario,
            'comentario': (
                'Tarea completada y transferida automáticamente.'
            ),
        },
    )

    if created:
        Usuario.objects.filter(pk=instance.usuario.pk).update(
            tareas_completadas=(
                models.F('tareas_completadas') + 1
            )
        )


class Evaluacion(models.Model):
    titulo = models.CharField(
        max_length=200,
        default='Título Predeterminado',
    )
    comentarios = models.TextField(
        default='Comentario pendiente',
    )
    fecha_evaluacion = models.DateTimeField(
        default=timezone.now,
    )
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    calificacion = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True,
    )
    tarea = models.OneToOneField(
        TareaPorDesarrollar,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'


class EvaluacionConfig(models.Model):
    tiempo_entrega = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=25.0,
    )
    complejidad_tarea = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=25.0,
    )
    cumplimiento_requerimientos = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=25.0,
    )
    calidad_codigo = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=25.0,
    )
    nota_maxima = models.IntegerField(default=100)

    def __str__(self):
        return 'Configuración de Evaluación'

    class Meta:
        verbose_name = 'Criterio Evaluación'
        verbose_name_plural = 'Criterios Evaluaciones'
