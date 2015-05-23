from django.db import models

# Create your models here.

class Actividade(models.Model):
    nombre = models.CharField(max_length = 200)
    tipo = models.CharField(max_length = 200)
    precio = models.CharField(max_length = 200)
    fecha = models.CharField(max_length = 200)
    hora_inicio = models.CharField(max_length = 200)
    duracion = models.CharField(max_length = 200)
    es_larga = models.CharField(max_length = 200)
    url = models.CharField(max_length = 200)

class Usuario(models.Model):
    nombre = models.CharField(max_length = 200,primary_key=True)
    actividad = models.ManyToManyField(Actividade)
    evento = models.CharField(max_length = 200)
    letra = models.CharField(max_length=200)
    fondo = models.CharField(max_length=200)
	
