from django.db import models
from django.contrib.auth.models import AbstractUser

# Creación de Modelos


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}"


class Proyecto(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('en pausa', 'En Pausa')
    ])

    def __str__(self):
        return self.nombre


class TareaPorDesarrollar(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('en progreso', 'En Progreso'),
        ('completada', 'Completada')])

    def __str__(self):
        return self.titulo


class TareaDesarrollada(models.Model):
    descripcion = models.TextField()
    fecha_entrega = models.DateTimeField()
    tarea_por_desarrollar = models.OneToOneField(
        TareaPorDesarrollar, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.tarea_por_desarrollar.titulo


class Evaluacion(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    fecha_evaluacion = models.DateField()
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    comentarios = models.TextField(null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Evaluación {self.id}"
