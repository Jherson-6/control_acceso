from django.urls import path, include
from . import views

app_name = 'docente'

urlpatterns = [
    path('', views.perfil, name='perfil'),
    path('AsignacionDocente-clases/', views.asignacionMaterias, name='asignacion'),
    path("reporte/", include("app.reporteAsistencia.urls")),
]