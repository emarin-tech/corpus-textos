# usuarios/pipeline.py

def mapear_campos_usuario(strategy, details, backend, user=None, *args, **kwargs):
    """
    - Copia details['email'] -> details['correo_electronico']
    - Genera un 'username' si falta (parte local del email)
    - IMPORTANTE: NO quitar details['email'] porque otros pasos lo usan
    """
    email = (details.get("email") or "").lower()
    if email:
        details["correo_electronico"] = email
        if not details.get("username"):
            details["username"] = email.split("@")[0][:150]
    return {"details": details}


def marcar_verificado(strategy, details, backend, user=None, *args, **kwargs):
    """
    Marca el correo como verificado si Google lo indica.
    Compatible con 'email_verified' y 'verified_email'.
    """
    if not user or backend.name != "google-oauth2":
        return {}

    resp = kwargs.get("response") or {}
    email_verificado = (
        resp.get("email_verified")
        if "email_verified" in resp
        else resp.get("verified_email")
    )

    if email_verificado and not getattr(user, "email_verificado", False):
        from django.utils import timezone
        user.email_verificado = True
        if hasattr(user, "email_verificado_en"):
            user.email_verificado_en = timezone.now()
            user.save(update_fields=["email_verificado", "email_verificado_en"])
        else:
            user.save(update_fields=["email_verificado"])

    return {}

def crear_usuario(strategy, details, backend, user=None, *args, **kwargs):
    """
    Crea un usuario nuevo SOLO con los campos que existen en tu modelo.
    Evita pasar first_name/last_name si tu modelo no los tiene.
    """
    if user:
        return {"user": user}

    # Obtén los campos que sí existen en tu modelo
    username = details.get("username")
    correo = details.get("correo_electronico") or details.get("email")

    # Construye kwargs válidos para tu Usuario.objects.create_user(...)
    datos = {}
    if username is not None:
        datos["username"] = username            # o el nombre real del campo (p. ej. "nombre_usuario")
    if correo is not None and "correo_electronico" in strategy.setting("USER_FIELDS", []):
        datos["correo_electronico"] = correo   # si tu modelo usa este nombre en lugar de "email"
    elif correo is not None and "email" in strategy.setting("USER_FIELDS", []):
        datos["email"] = correo

    # Si tu método create_user requiere otros campos obligatorios, añádelos aquí.

    nuevo = strategy.create_user(**datos)   # llama a Usuario.objects.create_user(**datos)
    return {"user": nuevo}
