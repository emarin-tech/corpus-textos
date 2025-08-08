# usuarios/utils.py
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from .tokens import email_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def enviar_email_verificacion(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_token_generator.make_token(user)  # <-- aquí
    url = reverse('usuarios:verificar_email', kwargs={'uidb64': uid, 'token': token})
    enlace = request.build_absolute_uri(url)

    destinatario = getattr(user, 'correo_electronico', None) or getattr(user, 'email', None)
    if not destinatario:
        print(">>> ERROR: usuario sin email/correo_electronico")
        return False

    asunto = 'Verifica tu correo en Corpus'
    mensaje = (
        f"Hola {getattr(user, 'nombre', '') or ''}\n\n"
        f"Confirma tu correo pulsando este enlace:\n{enlace}\n\n"
        "Si no fuiste tú, ignora este email."
    )
    print(">>> ENVIANDO VERIFICACION A:", destinatario, "ENLACE:", enlace)
    enviados = send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [destinatario])
    return enviados == 1
