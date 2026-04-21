from django.shortcuts import render, redirect
from app.estudiante.models import Estudiante
from app.academico.models import AsignacionDocente

def get_estudiante_actual(request):
    cod_usuario = request.session.get('usuario')

    if not cod_usuario:
        return None

    try:
        return Estudiante.objects.select_related(
            "usuario", "paralelo__semestre"
        ).get(usuario__codUsuario=cod_usuario)
    except Estudiante.DoesNotExist:
        return None



def perfil(request):
    cod_usuario = request.session.get('usuario')

    if not cod_usuario:
        return redirect('index')  # si no está logueado

    try:
        estudiante = Estudiante.objects.select_related("usuario").get(usuario__codUsuario=cod_usuario)
    except Estudiante.DoesNotExist:
        return redirect('index')

    return render(request, "estudiante/perfil.html", {"estudiante": estudiante})

def Asignacion_materias(request):
    estudiante = get_estudiante_actual(request)

    if not estudiante:
        return redirect('index')

    asignaciones = AsignacionDocente.objects.filter(
        paralelo=estudiante.paralelo
    ).select_related(
        "materia",
        "docente",
        "paralelo__aula",
        "paralelo__carrera",
        "paralelo__semestre",
        "horario"
    )

    return render(request, "estudiante/asignacion_materias.html", {
        "estudiante": estudiante,
        "asignaciones":asignaciones,
    })