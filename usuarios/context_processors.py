def contexto_corpus(request):
    user = getattr(request, "user", None)
    grupos = []
    activo = "personal"
    if user and user.is_authenticated:
        # TODO: adapta a tu modelo real de grupos/membresías
        # grupos = [{"slug": g.slug, "nombre": g.nombre} for g in user.grupos.all()]
        grupos = getattr(user, "grupos_sidebar", [])  # placeholder si aún no tienes modelo
        activo = getattr(request, "contexto_actual", "personal")
    return {"grupos_usuario": grupos, "contexto_actual": activo}