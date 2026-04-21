import face_recognition
import numpy as np
import json
import os
from django.conf import settings
from app.estudiante.models import Estudiante

def generar_encoding(ruta_relativa):
    ruta = os.path.join(settings.MEDIA_ROOT, ruta_relativa)

    if not os.path.exists(ruta):
        return None

    imagen = face_recognition.load_image_file(ruta)
    encodings = face_recognition.face_encodings(imagen)

    if len(encodings) > 0:
        return json.dumps(encodings[0].tolist())

    return None


def obtener_estudiantes_con_encoding():
    estudiantes = Estudiante.objects.exclude(encoding__isnull=True)

    data = []
    for est in estudiantes:
        encoding = np.array(json.loads(est.encoding))
        data.append((est, encoding))

    return data


def reconocer_estudiante(frame):
    # Convertir a RGB y asegurar tipo correcto
    rgb = np.ascontiguousarray(frame[:, :, ::-1], dtype=np.uint8)

    # Detectar rostros
    ubicaciones = face_recognition.face_locations(rgb)
    if not ubicaciones:
        return None

    try:
        encodings = face_recognition.face_encodings(rgb, ubicaciones)
    except Exception as e:
        # Evita que el servidor se caiga si hay error interno
        print("Error en face_encodings:", e)
        return None

    estudiantes_db = obtener_estudiantes_con_encoding()

    for encoding in encodings:
        for estudiante, encoding_db in estudiantes_db:
            # Usar distancia en lugar de compare_faces para mayor control
            distance = face_recognition.face_distance([encoding_db], encoding)[0]
            if distance < 0.5:  # tolerancia ajustable
                return estudiante

    return None
