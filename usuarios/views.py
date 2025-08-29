from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .forms import UsuarioPerfilForm, UsuarioPrivacidadForm, UsuarioCorreoForm
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.db import IntegrityError, connection
from django.contrib.auth.views import LoginView
from django.utils.http import urlsafe_base64_decode
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
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
                return redirect('corpus:inicio')

            except IntegrityError as e:
                print(">>> INTEGRITY ERROR:")
                traceback.print_exc()  # queremos ver QUÉ constraint salta
                form.add_error("email", "Ya existe una cuenta con este correo.")
            except Exception:
                traceback.print_exc()
                messages.warning(request, "Cuenta creada, pero no pudimos enviar el email de verificación ahora.")
                return redirect('corpus:inicio')
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
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)  # <-- usa el alias correcto
        messages.success(request, 'Correo verificado. ¡Bienvenido!')
        return redirect('corpus:escritorio')
    else:
        messages.error(request, 'Enlace inválido o caducado.')
        return redirect('corpus:inicio')  # evita mandar a 'dashboard' si no existe


def salir(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect('corpus:inicio')  # tu URL de la home

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")  # O 'email' si lo cambiaste en el form
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("corpus:escritorio")
        else:
            return render(request, "usuarios/login.html", {"form": form})
        #
        # if user is not None:
        #     auth_login(request, user)
        #     return redirect("corpus:escritorio")
        # else:
        #     return render(request, "usuarios/login.html", {
        #         "error": "Credenciales inválidas"
        #     })

    form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import UsuarioPerfilForm, UsuarioPrivacidadForm, UsuarioCorreoForm

@login_required
@require_http_methods(["GET", "POST"])
def ajustes_usuario(request):
    u = request.user
    seccion = request.POST.get("seccion")
    if request.method == "POST":
        # Inicializa todos SIN bind para poder rellenarlos luego según la sección
        perfil_form = UsuarioPerfilForm(instance=u)
        privacidad_form = UsuarioPrivacidadForm(instance=u)
        correo_form = UsuarioCorreoForm(instance=u, usuario=u)

        if seccion == "cuenta":
            perfil_form = UsuarioPerfilForm(request.POST, request.FILES, instance=u)  # para la foto
            correo_form = UsuarioCorreoForm(request.POST, instance=u, usuario=u)
            if perfil_form.is_valid() and correo_form.is_valid():
                perfil_form.save()
                if not correo_form.fields["correo_electronico"].disabled:
                    old = u.correo_electronico
                    usr = correo_form.save(commit=False)
                    if usr.correo_electronico != old:
                        usr.email_verificado = False
                    usr.save(update_fields=["correo_electronico", "email_verificado"])
                messages.success(request, "Cuenta actualizada.")
                return redirect("usuarios:ajustes")
            else:
                messages.error(request, "Revisa los campos: hay errores en el formulario.")

        elif seccion == "datos":
            perfil_form = UsuarioPerfilForm(request.POST, instance=u)
            if perfil_form.is_valid():
                perfil_form.save()
                messages.success(request, "Datos personales guardados.")
                return redirect("usuarios:ajustes")
            else:
                messages.error(request, "Revisa los campos: hay errores en el formulario.")

        elif seccion == "privacidad":
            privacidad_form = UsuarioPrivacidadForm(request.POST, instance=u)
            if privacidad_form.is_valid():
                privacidad_form.save()
                messages.success(request, "Preferencias actualizadas.")
                return redirect("usuarios:ajustes")
            else:
                messages.error(request, "Revisa los campos: hay errores en el formulario.")

        elif seccion == "direccion":
            perfil_form = UsuarioPerfilForm(request.POST, instance=u)
            if perfil_form.is_valid():
                perfil_form.save()
                messages.success(request, "Dirección guardada.")
                return redirect("usuarios:ajustes")
            else:
                messages.error(request, "Revisa los campos: hay errores en el formulario.")

    else:
        perfil_form = UsuarioPerfilForm(instance=u)
        privacidad_form = UsuarioPrivacidadForm(instance=u)
        correo_form = UsuarioCorreoForm(instance=u, usuario=u)

    return render(request, "usuarios/ajustes.html", {
        "perfil_form": perfil_form,
        "privacidad_form": privacidad_form,
        "correo_form": correo_form,
        "tiene_google": bool(getattr(u, "google_id", None)),
    })
