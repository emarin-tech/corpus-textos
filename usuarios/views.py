from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.db import IntegrityError, connection
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.conf import settings

from .forms import RegistroForm
from .models import Usuario
from .utils import enviar_email_verificacion
from .tokens import email_token_generator

import traceback


class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  # o pon tu ruta exacta

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        # lee el email del POST (antes de validar), para logs y pre-chequeo
        email_post = (request.POST.get("email") or "").strip().lower()

        # logs siempre
        print(">>> SETTINGS:", settings.SETTINGS_MODULE)
        print(">>> DB:", connection.get_connection_params())
        print(">>> POST KEYS:", list(request.POST.keys()))
        print(">>> email_post:", email_post)
        print(">>> existe_previo:", Usuario.objects.filter(correo_electronico__iexact=email_post).only("id").exists())

        if form.is_valid():
            email = form.cleaned_data["email"].strip().lower()
            password = form.cleaned_data["password1"]
            try:
                # OJO: usa el nombre que espera TU manager:
                # si tu manager acepta 'email=' mapeando a 'correo_electronico', usa email=
                user = Usuario.objects.create_user(
                    email=email,
                    password=password,
                    acepta_condiciones_servicio=form.cleaned_data["acepta_condiciones"],
                    email_verificado=False,
                )

                print(">>> CREATED PK:", user.pk)
                print(">>> EXISTS POST:", Usuario.objects.filter(correo_electronico__iexact=email).exists())

                user.is_active = False
                user.save(update_fields=["is_active"])

                enviar_email_verificacion(user, request)
                messages.success(request, "Cuenta creada. Revisa tu correo para verificarla.")
                return redirect("inicio")

            except IntegrityError as e:
                print(">>> INTEGRITY ERROR:")
                traceback.print_exc()  # queremos ver QUÉ constraint salta
                form.add_error("email", "Ya existe una cuenta con este correo.")
            except Exception:
                traceback.print_exc()
                messages.warning(request, "Cuenta creada, pero no pudimos enviar el email de verificación ahora.")
                return redirect("inicio")
        else:
            print(">>> FORM INVALID:", form.errors.as_json())
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = RegistroForm()

    return render(request, "usuarios/registro.html", {"form": form})

# ...

def verificar_email(request, uidb64, token):
    User = get_user_model()  # <-- define el modelo de usuario

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and email_token_generator.check_token(user, token):
        user.email_verificado = True
        user.is_active = True
        user.save(update_fields=['email_verificado', 'is_active'])
        auth_login(request, user)  # <-- usa el alias correcto
        messages.success(request, 'Correo verificado. ¡Bienvenido!')
        return redirect('inicio')  # o 'dashboard' si ya existe esa URL
    else:
        messages.error(request, 'Enlace inválido o caducado.')
        return redirect('dashboard')  # evita mandar a 'dashboard' si no existe


def salir(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect('inicio')  # tu URL de la home