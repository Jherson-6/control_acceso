from django.urls import path
from . import views

app_name = "reporteAsistencia"

urlpatterns = [
    path("global/", views.reporte_global, name="reporte_global"),
    path("diario/", views.reporte_diario, name="reporte_diario"),
    path("personal/<str:ru>/", views.reporte_personal, name="reporte_personal"),
    path("exportar/global/pdf/", views.exportar_global_pdf, name="exportar_global_pdf"),
    path("exportar/diario/pdf/", views.exportar_diario_pdf, name="exportar_diario_pdf"),
    path("exportar/personal/<str:ru>/pdf/", views.exportar_personal_pdf, name="exportar_personal_pdf"),
]