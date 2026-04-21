from datetime import datetime
from app.asistencia.models import Asistencia
from app.academico.models import AsignacionDocente


def obtener_dia_actual():
    dias = {
        0: "LU",
        1: "MA",
        2: "MI",
        3: "JU",
        4: "VI",
        5: "SA",
        6: "DO",
    }
    return dias[datetime.now().weekday()]


def registrar_asistencia(estudiante):
    ahora = datetime.now()
    hora_actual = ahora.time()
    dia_actual = obtener_dia_actual()

    # 🔥 Buscar todas las asignaciones del estudiante HOY
    asignaciones = AsignacionDocente.objects.filter(
        paralelo=estudiante.paralelo,
        horario__dia=dia_actual
    )

    for asignacion in asignaciones:
        inicio = asignacion.horario.hora_inicio
        fin = asignacion.horario.hora_fin

        # ✅ Validar si está dentro del horario
        if inicio <= hora_actual <= fin:

            # 🔥 Evitar duplicados SOLO en esa materia/horario
            existe = Asistencia.objects.filter(
                estudiante=estudiante,
                asignacion_docente=asignacion,
                fecha_ingreso=ahora.date()
            ).exists()

            if existe:
                return None, f"⚠️ Ya registraste asistencia en {asignacion.materia.nombre}"

            # ✅ Crear asistencia
            asistencia = Asistencia.objects.create(
                estudiante=estudiante,
                asignacion_docente=asignacion
            )

            return asistencia, f"✅ Asistencia registrada en {asignacion.materia.nombre}"

    # ❌ Si no está en ningún horario válido
    return None, "❌ No tienes clase en este horario"