from django.db.models import Q
from django.utils.dateparse import parse_date


def _parsear_fecha_filtro(valor):
    if not valor:
        return None

    try:
        return parse_date(valor)
    except ValueError:
        return None


def _filtrar_usuarios(
    queryset,
    termino='',
    fecha_alta_desde='',
    fecha_alta_hasta=''
):
    termino = (termino or '').strip()
    fecha_desde = _parsear_fecha_filtro(fecha_alta_desde)
    fecha_hasta = _parsear_fecha_filtro(fecha_alta_hasta)

    if termino:
        queryset = queryset.filter(
            Q(nombre__icontains=termino)
            | Q(apellido__icontains=termino)
            | Q(username__icontains=termino)
            | Q(email__icontains=termino)
        )

    if fecha_desde:
        queryset = queryset.filter(
            fecha_creacion__date__gte=fecha_desde
        )

    if fecha_hasta:
        queryset = queryset.filter(
            fecha_creacion__date__lte=fecha_hasta
        )

    return queryset


def _filtrar_proyectos(
    queryset,
    fecha_inicio_desde='',
    fecha_inicio_hasta='',
    proyecto_id='',
    titulo_palabras=''
):
    fecha_desde = _parsear_fecha_filtro(fecha_inicio_desde)
    fecha_hasta = _parsear_fecha_filtro(fecha_inicio_hasta)

    if fecha_desde:
        queryset = queryset.filter(
            fecha_inicio__gte=fecha_desde
        )

    if fecha_hasta:
        queryset = queryset.filter(
            fecha_inicio__lte=fecha_hasta
        )

    if proyecto_id:
        queryset = queryset.filter(id=proyecto_id)

    if titulo_palabras:
        queryset = queryset.filter(
            nombre__icontains=titulo_palabras
        )

    return queryset


def _filtrar_tareas(
    queryset,
    fecha_inicio_desde='',
    fecha_inicio_hasta='',
    tarea_id='',
    titulo_palabras=''
):
    fecha_desde = _parsear_fecha_filtro(fecha_inicio_desde)
    fecha_hasta = _parsear_fecha_filtro(fecha_inicio_hasta)

    if fecha_desde:
        queryset = queryset.filter(
            fecha_creacion__date__gte=fecha_desde
        )

    if fecha_hasta:
        queryset = queryset.filter(
            fecha_creacion__date__lte=fecha_hasta
        )

    if tarea_id:
        queryset = queryset.filter(id=tarea_id)

    if titulo_palabras:
        queryset = queryset.filter(
            titulo__icontains=titulo_palabras
        )

    return queryset