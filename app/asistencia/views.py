import base64
import numpy as np
import cv2
from django.shortcuts import render
from app.reconocimientoFacial.face_services import reconocer_estudiante
from app.asistencia.services import registrar_asistencia


def tomar_asistencia(request):
    if request.method == "POST":
        data_url = request.POST.get("imagen")

        if not data_url:
            return render(request, "asistencia/resultado.html", {
                "mensaje": "No se recibió imagen"
            })

        # 🔥 Convertir base64 a imagen OpenCV
        format, imgstr = data_url.split(';base64,')
        img_bytes = base64.b64decode(imgstr)

        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # 🧠 Reconocimiento facial
        estudiante = reconocer_estudiante(frame)

        if not estudiante:
            return render(request, "asistencia/resultado.html", {
                "mensaje": "No reconocido"
            })

        # 🔥 REGISTRAR ASISTENCIA (AQUÍ ESTABA EL ERROR)
        asistencia, mensaje = registrar_asistencia(estudiante)

        return render(request, "asistencia/resultado.html", {
            "mensaje": mensaje,
            "estudiante": estudiante,
            "asistencia": asistencia
        })

    return render(request, "asistencia/tomar_asistencia.html")