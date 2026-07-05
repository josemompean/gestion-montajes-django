from django.contrib import admin
from django.utils.html import format_html
from .models import Montaje, ModeloOrdenador, ComponenteHardware


class ComponenteHardwareAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'modelo', 'categoria_display', 'descripcion_corta')
    list_filter = ('categoria', 'marca')
    search_fields = ('nombre', 'marca', 'modelo', 'descripcion')
    list_per_page = 20
    
    def categoria_display(self, obj):
        return obj.get_categoria_display()
    categoria_display.short_description = 'Categoría'
    
    def descripcion_corta(self, obj):
        if obj.descripcion and len(obj.descripcion) > 50:
            return f"{obj.descripcion[:50]}..."
        return obj.descripcion
    descripcion_corta.short_description = 'Descripción'


class ModeloOrdenadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion_corta', 'activo', 'componentes_count')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    filter_horizontal = ('componentes',)  # Mejora la interfaz para seleccionar componentes
    
    def descripcion_corta(self, obj):
        if obj.descripcion and len(obj.descripcion) > 50:
            return f"{obj.descripcion[:50]}..."
        return obj.descripcion
    descripcion_corta.short_description = 'Descripción'
    
    def componentes_count(self, obj):
        return obj.componentes.count()
    componentes_count.short_description = 'Nº Componentes'


class MontajeAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'cliente', 'estado_display', 'fecha_montaje', 'montador', 'modelo_ordenador', 'duracion')
    list_filter = ('estado', 'montador')
    search_fields = ('numero_serie', 'cliente')
    # Eliminamos date_hierarchy para evitar problemas con zonas horarias
    # date_hierarchy = 'fecha_montaje'
    list_per_page = 20
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_serie', 'cliente', 'modelo_ordenador')
        }),
        ('Estado y Fechas', {
            'fields': ('estado', 'fecha_inicio', 'fecha_finalizacion')
        }),
        ('Asignación', {
            'fields': ('montador',)
        }),
    )
    
    def estado_display(self, obj):
        estados = {
            'Pendiente': 'red',
            'En proceso': 'orange',
            'Finalizado': 'green'
        }
        color = estados.get(obj.estado, 'gray')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.estado)
    estado_display.short_description = 'Estado'
    
    def duracion(self, obj):
        if obj.fecha_inicio and obj.fecha_finalizacion:
            duracion = obj.fecha_finalizacion - obj.fecha_inicio
            horas = duracion.total_seconds() // 3600
            minutos = (duracion.total_seconds() % 3600) // 60
            return f"{int(horas)}h {int(minutos)}m"
        return "-"
    duracion.short_description = 'Duración'


# Registrar los modelos en el panel de administración
admin.site.register(ComponenteHardware, ComponenteHardwareAdmin)
admin.site.register(ModeloOrdenador, ModeloOrdenadorAdmin)
admin.site.register(Montaje, MontajeAdmin)
