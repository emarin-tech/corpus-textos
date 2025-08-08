from django.contrib.auth.decorators import login_required
# corpus/views.py
import logging
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SuscripcionForm
# from .models import Suscripcion

logger = logging.getLogger(__name__)

def inicio(request):
    if request.method == "POST":
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            email_usuario = form.cleaned_data["email"]

            # Guardar en BD (opcional)
            # Suscripcion.objects.get_or_create(email=email_usuario)

            try:
                enviar_suscripcion(email_usuario)
            except BadHeaderError:
                logger.exception("Cabecera inválida en envío de suscripción")
                messages.error(request, "No se ha podido mandar el mensaje por un error de cabecera.")
                return redirect("inicio")
            except Exception:
                logger.exception("Error enviando suscripción")
                messages.error(request, "No se ha podido mandar el mensaje. Inténtalo más tarde.")
                return redirect("inicio")

            messages.success(request, "Mensaje enviado, ¡gracias por suscribirte!")
            return redirect("inicio")
    else:
        form = SuscripcionForm()

    return render(request, "corpus/inicio.html", {"form": form})

def enviar_suscripcion(email_usuario: str) -> None:
    asunto = "[Corpus] Nueva suscripción"
    cuerpo = (
        "Hola Eduardo,\n\n"
        "Un nuevo usuario se ha suscrito desde la web:\n\n"
        f"Correo: {email_usuario}\n"
        "Fecha: automática al recibir\n\n"
        "— Sistema Corpus"
    )

    send_mail(
        subject=asunto,
        message=cuerpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["info@emarintech.com"],
        fail_silently=False,
    )


@login_required
def dashboard(request):
    return render(request, "dashboard.html")

