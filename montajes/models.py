from django.db import models
from django.contrib.auth.models import User

class ComponenteHardware(models.Model):
    """Modelo para representar componentes de hardware"""
    CATEGORIA_CHOICES = [
        ('CPU', 'Procesador'),
        ('RAM', 'Memoria RAM'),
        ('GPU', 'Tarjeta Gráfica'),
        ('SSD', 'Disco SSD'),
        ('HDD', 'Disco Duro'),
        ('MOB', 'Placa Base'),
        ('PSU', 'Fuente de Alimentación'),
        ('COOL', 'Sistema de Refrigeración'),
        ('CASE', 'Caja/Chasis'),
        ('OTHER', 'Otro')
    ]
    
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_categoria_display()}: {self.marca} {self.modelo}"

class ModeloOrdenador(models.Model):
    """Modelo para representar modelos de ordenadores"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    componentes = models.ManyToManyField(ComponenteHardware, related_name='modelos_ordenador')
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Montaje(models.Model):
    numero_serie = models.CharField(max_length=50, unique=True)
    cliente = models.CharField(max_length=100)
    fecha_montaje = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('En proceso', 'En proceso'), ('Finalizado', 'Finalizado')]
    )
    montador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='montajes')
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    modelo_ordenador = models.ForeignKey(ModeloOrdenador, on_delete=models.SET_NULL, null=True, blank=True, related_name='montajes')
    
    def __str__(self):
        return f"{self.numero_serie} - {self.estado}"
