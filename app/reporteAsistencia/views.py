from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from app.asistencia.models import Asistencia
from app.estudiante.models import Estudiante

# --- Reportes en pantalla ---
def reporte_global(request):
    asistencias = Asistencia.objects.all().order_by("-fecha_ingreso", "-hora_ingreso")
    return render(request, "reporteAsistencia/reporte_global.html", {
        "asistencias": asistencias,
    })

def reporte_diario(request):
    hoy = timezone.now().date()
    asistencias = Asistencia.objects.filter(fecha_ingreso=hoy).order_by("-hora_ingreso")
    return render(request, "reporteAsistencia/reporte_diario.html", {
        "asistencias": asistencias,
        "hoy": hoy
    })

def reporte_personal(request, ru):
    estudiante = Estudiante.objects.get(RU=ru)
    asistencias = Asistencia.objects.filter(estudiante=estudiante).order_by("-fecha_ingreso")
    return render(request, "reporteAsistencia/reporte_personal.html", {
        "estudiante": estudiante,
        "asistencias": asistencias,
    })

# -----------------------Exportar a PDF-------------------------
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type="application/pdf")
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=400)
    return response

def exportar_global_pdf(request):
    asistencias = Asistencia.objects.all()
    return render_to_pdf("reporteAsistencia/pdf_global.html", {
        "asistencias": asistencias,
    })

def exportar_diario_pdf(request):
    hoy = timezone.now().date()
    asistencias = Asistencia.objects.filter(fecha_ingreso=hoy)
    return render_to_pdf("reporteAsistencia/pdf_diario.html", {
        "asistencias": asistencias,
        "hoy": hoy
    })

def exportar_personal_pdf(request, ru):
    estudiante = Estudiante.objects.get(RU=ru)
    asistencias = Asistencia.objects.filter(estudiante=estudiante)
    return render_to_pdf("reporteAsistencia/pdf_personal.html", {
        "estudiante": estudiante,
        "asistencias": asistencias,
    })
