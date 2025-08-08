def map_user_fields(strategy, details, backend, user=None, *args, **kwargs):
    """
    - Copia details['email'] -> details['correo_electronico']
    - Genera un 'username' si falta (parte local del email)
    - IMPORTANTE: NO quites details['email'] porque otros pasos lo usan
    """
    email = (details.get("email") or "").lower()
    if email:
        details["correo_electronico"] = email
        if not details.get("username"):
            details["username"] = email.split("@")[0][:150]
    return {"details": details}

def mark_verified(strategy, details, backend, user=None, *args, **kwargs):
    email_verified = kwargs.get("response", {}).get("email_verified")
    if user and email_verified:
        if not getattr(user, "email_verificado", False):
            user.email_verificado = True
            from django.utils import timezone
            user.email_verificado_en = timezone.now()
            user.save(update_fields=["email_verificado", "email_verificado_en"])
    return {}