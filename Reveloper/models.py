from django.db import models
from django.contrib.auth.models import AbstractUser

# Creación de Modelos


class Usuario(AbstractUser):
    # Agregar campos adicionales específicos para los usuarios
    pass


class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


class TareaPorDesarrollar(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()
    estado = models.CharField(max_length=20)


class TareaDesarrollada(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()
    estado = models.CharField(max_length=20)


class Evaluacion(models.Model):
    tarea_desarrollada = models.ForeignKey(
        TareaDesarrollada, on_delete=models.CASCADE)
    calificacion = models.IntegerField()
    comentario = models.TextField()
    fecha_evaluacion = models.DateField()
