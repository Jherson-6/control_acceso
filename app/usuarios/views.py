from django.shortcuts import render, redirect
from .models import Usuario
from app.estudiante.models import Estudiante
from app.docente.models import Docente
from app.direccionCarrera.models import DireccionCarrera
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        codigo = form.cleaned_data['codigo']
        password = form.cleaned_data['password']
        try:
            user = Usuario.objects.get(codUsuario=codigo)
            if user.password == password:
                # GUARDAR SESIÓN (CLAVE)
                request.session['usuario'] = user.codUsuario
                
                if Estudiante.objects.filter(usuario=user).exists():
                    return redirect('estudiante:perfil')

                elif Docente.objects.filter(usuario=user).exists():
                    return redirect('docente:perfil')

                elif DireccionCarrera.objects.filter(usuario=user).exists():
                    return redirect('direccionCarrera:perfil')

                else:
                    return render(request, "usuarios/login.html", {
                        "form": form,
                        "error": "Usuario sin tipo"
                    })

            else:
                return render(request, "usuarios/login.html", {
                    "form": form,
                    "error": "Contraseña incorrecta"
                })

        except Usuario.DoesNotExist:
            return render(request, "usuarios/login.html", { "form": form, "error": "El usuario no existe"})
    return render(request, "usuarios/login.html", {"form": form})