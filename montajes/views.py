from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import RegistroForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Montaje
import json
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
import calendar
from calendar import monthrange

# Vista de Registro
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data["password1"])
            usuario.save()
            login(request, usuario)
            return redirect("lista_montajes")  # Redirige después del registro
    else:
        form = RegistroForm()
    return render(request, "montajes/registro.html", {"form": form})

# Vista de Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect("lista_montajes")
    else:
        form = AuthenticationForm()
    return render(request, "montajes/login.html", {"form": form})

# Vista de Logout
def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect("login")

@login_required
def lista_montajes(request):
    """Vista para mostrar montajes pendientes que pueden ser iniciados por cualquier montador"""
    # Obtener parámetros de filtrado y ordenación
    busqueda = request.GET.get('busqueda', '')
    orden = request.GET.get('orden', '-fecha_montaje')  # Por defecto, ordena por fecha descendente
    
    # Filtrar montajes pendientes
    montajes = Montaje.objects.filter(estado='Pendiente')
    
    # Aplicar filtro de búsqueda si existe
    if busqueda:
        montajes = montajes.filter(
            Q(numero_serie__icontains=busqueda) | 
            Q(cliente__icontains=busqueda)
        )
    
    # Aplicar ordenación
    valid_order_fields = ['fecha_montaje', '-fecha_montaje', 'cliente', '-cliente', 'numero_serie', '-numero_serie']
    if orden in valid_order_fields:
        montajes = montajes.order_by(orden)
    else:
        montajes = montajes.order_by('-fecha_montaje')  # Orden por defecto
    
    context = {
        'active_menu': 'montajes',
        'montajes': montajes,
        'busqueda': busqueda,
        'orden_actual': orden,
    }
    
    return render(request, "montajes/lista_montajes.html", context)

@login_required
def mis_montajes(request):
    """Vista para mostrar los montajes asignados al usuario actual"""
    # Obtener parámetros de filtrado y ordenación
    busqueda = request.GET.get('busqueda', '')
    estado_filtro = request.GET.get('estado', '')
    orden = request.GET.get('orden', '-fecha_montaje')
    
    # Obtener los montajes del usuario actual
    montajes = Montaje.objects.filter(montador=request.user)
    
    # Aplicar filtro de búsqueda si existe
    if busqueda:
        montajes = montajes.filter(
            Q(numero_serie__icontains=busqueda) | 
            Q(cliente__icontains=busqueda)
        )
    
    # Aplicar filtro por estado si se especifica
    if estado_filtro and estado_filtro in ['En proceso', 'Finalizado']:
        montajes = montajes.filter(estado=estado_filtro)
    
    # Aplicar ordenación
    valid_order_fields = ['fecha_montaje', '-fecha_montaje', 'cliente', '-cliente', 
                         'numero_serie', '-numero_serie', 'fecha_inicio', '-fecha_inicio',
                         'fecha_finalizacion', '-fecha_finalizacion']
    if orden in valid_order_fields:
        montajes = montajes.order_by(orden)
    else:
        montajes = montajes.order_by('-fecha_montaje')  # Orden por defecto
    
    # Separar por estados para la vista (mantenemos la lógica existente)
    montajes_en_proceso = montajes.filter(estado='En proceso')
    montajes_finalizados = montajes.filter(estado='Finalizado')
    
    # Si hay un filtro de búsqueda o estado, no separamos por estados
    if busqueda or estado_filtro:
        context = {
            'active_menu': 'mis_montajes',
            'montajes_filtrados': montajes,
            'busqueda': busqueda,
            'estado_filtro': estado_filtro,
            'orden_actual': orden,
            'modo_filtro': True,
            # Agregar conteos totales para las tarjetas de resumen
            'montajes_en_proceso': Montaje.objects.filter(montador=request.user, estado='En proceso'),
            'montajes_finalizados': Montaje.objects.filter(montador=request.user, estado='Finalizado'),
        }
    else:
        # Paginar los montajes finalizados
        paginator = Paginator(montajes_finalizados, 10)  # Mostrar 10 montajes por página
        page_number = request.GET.get('page')
        montajes_finalizados_paginados = paginator.get_page(page_number)
        
        context = {
            'active_menu': 'mis_montajes',
            'montajes_en_proceso': montajes_en_proceso,
            'montajes_finalizados': montajes_finalizados_paginados,
            'busqueda': busqueda,
            'estado_filtro': estado_filtro,
            'orden_actual': orden,
            'modo_filtro': False,
            # Agregar conteos totales para las tarjetas de resumen
            'total_montajes_en_proceso': montajes_en_proceso.count(),
            'total_montajes_finalizados': montajes_finalizados.count(),
        }
    
    # Comprobar si es una solicitud AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, "montajes/mis_montajes.html", context)
    
    return render(request, "montajes/mis_montajes.html", context)

@login_required
def iniciar_montaje(request, montaje_id):
    """Vista para iniciar un montaje y asignarlo al usuario actual"""
    montaje = get_object_or_404(Montaje, id=montaje_id)
    
    # Verificar que el montaje esté pendiente
    if montaje.estado != 'Pendiente':
        messages.error(request, "Este montaje ya ha sido iniciado por otro montador.")
        return redirect('lista_montajes')
    
    # Asignar al usuario actual
    montaje.montador = request.user
    montaje.estado = 'En proceso'
    montaje.fecha_inicio = timezone.now()
    montaje.save()
    
    messages.success(request, f"Has iniciado el montaje {montaje.numero_serie} correctamente.")
    return redirect('mis_montajes')

@login_required
def finalizar_montaje(request, montaje_id):
    """Vista para finalizar un montaje"""
    montaje = get_object_or_404(Montaje, id=montaje_id)
    
    # Verificar que el montaje pertenezca al usuario actual
    if montaje.montador != request.user:
        messages.error(request, "No tienes permiso para finalizar este montaje.")
        return redirect('mis_montajes')
    
    # Verificar que el montaje esté en proceso
    if montaje.estado != 'En proceso':
        messages.error(request, "Solo puedes finalizar montajes en proceso.")
        return redirect('mis_montajes')
    
    # Finalizar el montaje
    montaje.estado = 'Finalizado'
    montaje.fecha_finalizacion = timezone.now()
    montaje.save()
    
    messages.success(request, f"Has finalizado el montaje {montaje.numero_serie} correctamente.")
    return redirect('mis_montajes')

@login_required
def historial_montajes(request):
    """Vista para mostrar el historial de montajes del montador que ha iniciado sesión"""
    # Obtener solo los montajes del montador que ha iniciado sesión
    montajes = Montaje.objects.filter(montador=request.user).order_by('-fecha_montaje')
    
    # Obtener todos los montajes finalizados del usuario actual
    montajes_finalizados = Montaje.objects.filter(
        montador=request.user,
        estado='Finalizado',
        fecha_finalizacion__isnull=False
    )
    
    # Fecha actual para cálculos
    hoy = timezone.now().date()
    
    # Inicializar contadores
    montajes_hoy = 0
    montajes_semana = 0
    montajes_mes = 0
    
    # Calcular inicio de semana y mes
    inicio_semana = hoy - timedelta(days=6)
    inicio_mes = hoy - timedelta(days=29)
    
    # Contar manualmente para evitar problemas con el filtrado de fechas
    for montaje in montajes_finalizados:
        # Convertir la fecha de finalización a date para comparar
        fecha_fin = montaje.fecha_finalizacion.date()
        
        # Contar montajes de hoy
        if fecha_fin == hoy:
            montajes_hoy += 1
        
        # Contar montajes de la semana (incluye hoy)
        if inicio_semana <= fecha_fin <= hoy:
            montajes_semana += 1
        
        # Contar montajes del mes (incluye hoy)
        if inicio_mes <= fecha_fin <= hoy:
            montajes_mes += 1
    
    # Total de montajes finalizados
    montajes_totales = montajes_finalizados.count()
    
    context = {
        'active_menu': 'historial',
        'montajes': montajes,
        'estadisticas': {
            'hoy': montajes_hoy,
            'semana': montajes_semana,
            'mes': montajes_mes,
            'totales': montajes_totales
        }
    }
    
    return render(request, 'montajes/historial.html', context)

@login_required
def detalle_montaje(request, montaje_id):
    """Vista para mostrar los detalles de un montaje específico"""
    montaje = get_object_or_404(Montaje, id=montaje_id)
    
    # Preparar contexto con el montaje y sus datos
    context = {
        'active_menu': 'montajes' if montaje.estado == 'Pendiente' else 'mis_montajes',
        'montaje': montaje,
    }
    
    # Si el montaje tiene un modelo de ordenador asignado, incluir sus componentes
    if montaje.modelo_ordenador:
        # Obtenemos los componentes ordenados por categoría
        componentes = montaje.modelo_ordenador.componentes.all().order_by('categoria')
        context['componentes'] = componentes
    
    return render(request, 'montajes/detalle_montaje.html', context)

@login_required
def historial_admin(request):
    """Vista para que los administradores vean el rendimiento de cada montador"""
    # Verificar que el usuario sea administrador
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect('lista_montajes')
    
    # Obtener parámetros de filtrado
    periodo = request.GET.get('periodo', 'mes')  # Por defecto mostrar datos del último mes
    busqueda = request.GET.get('busqueda', '')
    
    # Fecha actual para cálculos
    ahora = timezone.now()
    hoy = ahora.date()
    
    # Definir el rango de fechas según el periodo seleccionado
    if periodo == 'dia':
        # Inicio: hoy a las 00:00
        fecha_inicio = datetime(hoy.year, hoy.month, hoy.day, 0, 0, 0, tzinfo=ahora.tzinfo)
        # Fin: hoy a las 23:59:59
        fecha_fin = datetime(hoy.year, hoy.month, hoy.day, 23, 59, 59, tzinfo=ahora.tzinfo)
        titulo_periodo = "Último día"
    elif periodo == 'semana':
        # Inicio: hace 7 días a las 00:00
        fecha_hace_7_dias = hoy - timedelta(days=6)
        fecha_inicio = datetime(fecha_hace_7_dias.year, fecha_hace_7_dias.month, fecha_hace_7_dias.day, 0, 0, 0, tzinfo=ahora.tzinfo)
        # Fin: hoy a las 23:59:59
        fecha_fin = datetime(hoy.year, hoy.month, hoy.day, 23, 59, 59, tzinfo=ahora.tzinfo)
        titulo_periodo = "Última semana"
    elif periodo == 'mes':
        # Inicio: hace 30 días a las 00:00
        fecha_hace_30_dias = hoy - timedelta(days=29)
        fecha_inicio = datetime(fecha_hace_30_dias.year, fecha_hace_30_dias.month, fecha_hace_30_dias.day, 0, 0, 0, tzinfo=ahora.tzinfo)
        # Fin: hoy a las 23:59:59
        fecha_fin = datetime(hoy.year, hoy.month, hoy.day, 23, 59, 59, tzinfo=ahora.tzinfo)
        titulo_periodo = "Último mes"
    elif periodo == 'trimestre':
        # Inicio: hace 90 días a las 00:00
        fecha_hace_90_dias = hoy - timedelta(days=89)
        fecha_inicio = datetime(fecha_hace_90_dias.year, fecha_hace_90_dias.month, fecha_hace_90_dias.day, 0, 0, 0, tzinfo=ahora.tzinfo)
        # Fin: hoy a las 23:59:59
        fecha_fin = datetime(hoy.year, hoy.month, hoy.day, 23, 59, 59, tzinfo=ahora.tzinfo)
        titulo_periodo = "Último trimestre"
    elif periodo == 'año':
        # Inicio: hace 365 días a las 00:00
        fecha_hace_365_dias = hoy - timedelta(days=364)
        fecha_inicio = datetime(fecha_hace_365_dias.year, fecha_hace_365_dias.month, fecha_hace_365_dias.day, 0, 0, 0, tzinfo=ahora.tzinfo)
        # Fin: hoy a las 23:59:59
        fecha_fin = datetime(hoy.year, hoy.month, hoy.day, 23, 59, 59, tzinfo=ahora.tzinfo)
        titulo_periodo = "Último año"
    else:  # todos
        fecha_inicio = None
        fecha_fin = None
        titulo_periodo = "Todo el tiempo"
    
    # Importar User desde django.contrib.auth.models
    from django.contrib.auth.models import User
    
    # Obtener todos los montadores (usuarios que han realizado al menos un montaje)
    montadores = User.objects.filter(montajes__isnull=False).distinct()
    
    # Aplicar filtro de búsqueda si existe
    if busqueda:
        montadores = montadores.filter(
            Q(username__icontains=busqueda) | 
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda)
        )
    
    # Datos de rendimiento para cada montador
    rendimiento_montadores = []
    
    for montador in montadores:
        # Filtrar montajes por montador y periodo
        if fecha_inicio and fecha_fin:
            montajes_montador = Montaje.objects.filter(
                montador=montador, 
                fecha_montaje__gte=fecha_inicio,
                fecha_montaje__lte=fecha_fin,
            )
        else:
            montajes_montador = Montaje.objects.filter(montador=montador)
        
        # Contar montajes finalizados
        montajes_finalizados = montajes_montador.filter(estado='Finalizado').count()
        
        # Contar montajes en proceso
        montajes_en_proceso = montajes_montador.filter(estado='En proceso').count()
        
        # Calcular tiempo promedio de montaje (solo para montajes finalizados)
        tiempo_promedio = None
        montajes_con_tiempo = montajes_montador.filter(
            estado='Finalizado',
            fecha_inicio__isnull=False,
            fecha_finalizacion__isnull=False
        )
        
        if montajes_con_tiempo.exists():
            total_segundos = 0
            for m in montajes_con_tiempo:
                duracion = m.fecha_finalizacion - m.fecha_inicio
                total_segundos += duracion.total_seconds()
            
            # Calcular promedio y convertir a formato legible
            if montajes_con_tiempo.count() > 0:
                promedio_segundos = total_segundos / montajes_con_tiempo.count()
                # Convertir a días, horas, minutos
                dias = int(promedio_segundos // 86400)
                horas = int((promedio_segundos % 86400) // 3600)
                minutos = int((promedio_segundos % 3600) // 60)
                
                tiempo_promedio = f"{dias}d {horas}h {minutos}m"
        
        # Añadir datos a la lista si hay montajes en el periodo o si estamos mostrando todos
        if montajes_finalizados > 0 or montajes_en_proceso > 0 or periodo == 'todos':
            rendimiento_montadores.append({
                'montador': montador,
                'finalizados': montajes_finalizados,
                'en_proceso': montajes_en_proceso,
                'total': montajes_finalizados + montajes_en_proceso,
                'tiempo_promedio': tiempo_promedio
            })
    
    # Ordenar por número total de montajes (descendente)
    rendimiento_montadores.sort(key=lambda x: x['total'], reverse=True)
    
    context = {
        'active_menu': 'historial_admin',
        'rendimiento_montadores': rendimiento_montadores,
        'periodo': periodo,
        'titulo_periodo': titulo_periodo,
        'busqueda': busqueda,
    }
    
    return render(request, 'montajes/historial_admin.html', context)

@login_required
def estadisticas_montajes(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect('lista_montajes')

    periodo = request.GET.get('periodo', 'mes')
    montador_id = request.GET.get('montador', 'global')
    
    # Obtener fecha y hora actual con timezone
    ahora = timezone.now()
    hoy = ahora.date()
    
    etiquetas_chart = []
    datos_chart = []
    titulo_periodo_display = ""
    fecha_inicio = None
    fecha_fin = None

    if periodo == 'dia':
        titulo_periodo_display = "Últimos 30 días"
        
        # Inicializar datos para los últimos 30 días
        temp_data_map = {}
        for i in range(30):
            current_date = hoy - timedelta(days=i)
            etiquetas_chart.insert(0, current_date.strftime("%d/%m")) # Más antiguo primero
            
            # Crear fecha con timezone para cada día
            dt_inicio = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0, tzinfo=ahora.tzinfo)
            dt_fin = datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59, tzinfo=ahora.tzinfo)
            
            # Contar montajes para este día
            montajes_query = Montaje.objects.filter(
                fecha_montaje__gte=dt_inicio,
                fecha_montaje__lte=dt_fin
            )
            
            # Filtrar por montador si se ha seleccionado uno específico
            if montador_id != 'global' and montador_id.isdigit():
                montajes_query = montajes_query.filter(montador_id=int(montador_id))
                
            montajes_dia = montajes_query.count()
            
            datos_chart.insert(0, montajes_dia)  # Insertar en el mismo orden que las etiquetas

        # Fecha inicial para mostrar en la vista (30 días atrás)
        fecha_hace_30_dias = hoy - timedelta(days=29)
        fecha_inicio = datetime(fecha_hace_30_dias.year, fecha_hace_30_dias.month, fecha_hace_30_dias.day, 0, 0, 0, tzinfo=ahora.tzinfo)
        fecha_fin = datetime(hoy.year, hoy.month, hoy.day, 23, 59, 59, tzinfo=ahora.tzinfo)

    elif periodo == 'semana':
        titulo_periodo_display = "Últimas 12 semanas"
        
        # Preparar datos para las últimas 12 semanas
        datos_chart = []
        for i in range(12):
            # Obtener fecha dentro de la semana i-ésima atrás (0 es la semana actual)
            semana_actual = hoy - timedelta(weeks=(11-i))
            
            # Calcular inicio y fin de la semana
            inicio_semana = semana_actual - timedelta(days=semana_actual.weekday())  # Lunes
            fin_semana = inicio_semana + timedelta(days=6)  # Domingo
            
            # Convertir a datetime con timezone
            dt_inicio = datetime(inicio_semana.year, inicio_semana.month, inicio_semana.day, 0, 0, 0, tzinfo=ahora.tzinfo)
            dt_fin = datetime(fin_semana.year, fin_semana.month, fin_semana.day, 23, 59, 59, tzinfo=ahora.tzinfo)
            
            # Contar montajes para esta semana
            montajes_query = Montaje.objects.filter(
                fecha_montaje__gte=dt_inicio,
                fecha_montaje__lte=dt_fin
            )
            
            # Filtrar por montador si se ha seleccionado uno específico
            if montador_id != 'global' and montador_id.isdigit():
                montajes_query = montajes_query.filter(montador_id=int(montador_id))
                
            montajes_semana = montajes_query.count()
            
            datos_chart.append(montajes_semana)
            etiquetas_chart.append(f"Sem {semana_actual.strftime('%W')} ({inicio_semana.strftime('%d/%m')})")
        
        # Fecha inicial para mostrar en la vista (12 semanas atrás)
        fecha_hace_12_semanas = hoy - timedelta(weeks=11)
        lunes_12_semanas = fecha_hace_12_semanas - timedelta(days=fecha_hace_12_semanas.weekday())
        fecha_inicio = datetime(lunes_12_semanas.year, lunes_12_semanas.month, lunes_12_semanas.day, 0, 0, 0, tzinfo=ahora.tzinfo)
        fecha_fin = datetime(hoy.year, hoy.month, hoy.day, 23, 59, 59, tzinfo=ahora.tzinfo)

    elif periodo == 'mes':
        titulo_periodo_display = "Últimos 12 meses"
        
        # Preparar datos para los últimos 12 meses
        datos_chart = []
        for i in range(12):
            # Calcular el mes i-ésimo atrás
            month_offset = 11 - i
            target_month = hoy.month - month_offset
            target_year = hoy.year
            
            # Ajustar año si el mes es negativo
            while target_month <= 0:
                target_month += 12
                target_year -= 1
                
            # Primer día del mes
            primer_dia = datetime(target_year, target_month, 1, tzinfo=ahora.tzinfo)
            
            # Último día del mes
            if target_month == 12:
                ultimo_dia = datetime(target_year + 1, 1, 1, tzinfo=ahora.tzinfo) - timedelta(days=1)
            else:
                ultimo_dia = datetime(target_year, target_month + 1, 1, tzinfo=ahora.tzinfo) - timedelta(days=1)
            
            # Convertir a datetime con timezone completo
            dt_inicio = datetime(primer_dia.year, primer_dia.month, primer_dia.day, 0, 0, 0, tzinfo=ahora.tzinfo)
            dt_fin = datetime(ultimo_dia.year, ultimo_dia.month, ultimo_dia.day, 23, 59, 59, tzinfo=ahora.tzinfo)
            
            # Contar montajes para este mes
            montajes_query = Montaje.objects.filter(
                fecha_montaje__gte=dt_inicio,
                fecha_montaje__lte=dt_fin
            )
            
            # Filtrar por montador si se ha seleccionado uno específico
            if montador_id != 'global' and montador_id.isdigit():
                montajes_query = montajes_query.filter(montador_id=int(montador_id))
                
            montajes_mes = montajes_query.count()
            
            datos_chart.append(montajes_mes)
            
            # Nombre del mes en español para la etiqueta
            nombre_mes = primer_dia.strftime("%B").capitalize()
            meses_es = {
                "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
                "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
                "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
            }
            nombre_mes_es = meses_es.get(nombre_mes, nombre_mes)
            etiquetas_chart.append(f"{nombre_mes_es} {primer_dia.year}")
        
        # Fecha inicial para mostrar en la vista (12 meses atrás)
        month = hoy.month - 11
        year = hoy.year
        while month <= 0:
            month += 12
            year -= 1
        fecha_inicio = datetime(year, month, 1, 0, 0, 0, tzinfo=ahora.tzinfo)
        
        # Último día del mes actual
        if hoy.month == 12:
            fecha_fin = datetime(hoy.year + 1, 1, 1, 0, 0, 0, tzinfo=ahora.tzinfo) - timedelta(seconds=1)
        else:
            fecha_fin = datetime(hoy.year, hoy.month + 1, 1, 0, 0, 0, tzinfo=ahora.tzinfo) - timedelta(seconds=1)
    else:
        return redirect('estadisticas_montajes') # Redirigir si el periodo no es válido

    # Calcular estadísticas adicionales
    total_montajes_periodo = sum(datos_chart)
    promedio_montajes = round(total_montajes_periodo / len(datos_chart), 1) if datos_chart else 0
    max_montajes = max(datos_chart) if datos_chart else 0
    periodo_max_montajes = "N/A"
    if max_montajes > 0:
        try:
            indice_max = datos_chart.index(max_montajes)
            periodo_max_montajes = etiquetas_chart[indice_max]
        except (ValueError, IndexError):
            periodo_max_montajes = "Error"
            
    # Obtener todos los montadores para el selector
    montadores = User.objects.filter(is_staff=True)
    
    # Obtener el nombre del montador seleccionado para mostrar en el título
    nombre_montador = "Global"
    if montador_id != 'global' and montador_id.isdigit():
        try:
            montador = User.objects.get(id=int(montador_id))
            nombre_montador = montador.username
        except User.DoesNotExist:
            nombre_montador = "Desconocido"
    
    context = {
        'active_menu': 'estadisticas_montajes',
        'periodo': periodo,
        'titulo_periodo': titulo_periodo_display,
        'fechas': json.dumps(etiquetas_chart),
        'totales': json.dumps(datos_chart),
        'total_montajes': total_montajes_periodo,
        'promedio': promedio_montajes,
        'maximo': max_montajes,
        'periodo_maximo': periodo_max_montajes,
        'montadores': montadores,
        'montador_id': montador_id,
        'nombre_montador': nombre_montador,
    }
    return render(request, 'montajes/estadisticas_montajes.html', context)