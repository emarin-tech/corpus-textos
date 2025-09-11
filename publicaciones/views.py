from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from .forms import AutorForm
from .models import Autor
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404


from django.views.decorators.csrf import csrf_exempt  # opcional si tienes problemas con el token

def autores_inicio(request):
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES)
        if form.is_valid():
            autor = form.save(commit=False)
            autor.creado_por = request.user
            autor.modificado_por = request.user
            autor.propietario_usuario = request.user
            if hasattr(request.user, 'grupo_activo'):
                autor.propietario_grupo = request.user.grupo_activo
            autor.save()
            return redirect('publicaciones:autores_inicio')  # recarga el escritorio
    else:
        form = AutorForm()

    return render(request, 'publicaciones/autores/inicio.html', {'form': form})


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import AutorForm
import logging, traceback

logger = logging.getLogger(__name__)

@login_required
@require_http_methods(["GET", "POST"])
def crear_autor(request):
    if request.method == "GET":
        form = AutorForm()
        return render(request, 'publicaciones/autores/crear.html', {'form': form})

    # POST → AJAX
    try:
        form = AutorForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({'success': False, 'errores': form.errors}, status=400)

        autor = form.save(commit=False)
        if hasattr(autor, 'creado_por_id'):
            autor.creado_por = request.user
        autor.save()
        return JsonResponse({'success': True, 'id': autor.id, 'nombre': autor.nombre, 'apellidos': autor.apellidos}, status=201)

    except Exception as e:
        logger.error("Error creando autor: %s\n%s", e, traceback.format_exc())
        return JsonResponse({'success': False, 'mensaje': 'Error interno'}, status=500)


def autores_ajax(request):
    autores = Autor.objects.all().order_by('apellidos')
    paginator = Paginator(autores, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'publicaciones/partials/lista_autores_ajax.html', {
        'page_obj': page_obj
    })



def editar_autor(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            autor = Autor.objects.get(pk=pk)
        except Autor.DoesNotExist:
            raise Http404("Autor no encontrado")

        form = AutorForm(request.POST, request.FILES, instance=autor)
        if form.is_valid():
            autor = form.save(commit=False)
            autor.modificado_por = request.user
            autor.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required
@require_POST
def eliminar_autor(request, pk):
    autor = get_object_or_404(Autor, pk=pk)

    # ¿tiene publicaciones/fuentes?
    relacionados = getattr(autor, 'fuentes', None)
    count = relacionados.count() if relacionados else 0

    if count > 0:
        # 409 Conflict: no se puede borrar por dependencias
        return JsonResponse({
            'success': False,
            'bloqueado': True,
            'count': count,
            'mensaje': f'No se puede borrar: tiene {count} fuente(s) vinculada(s).'
        }, status=409)

    # sin dependencias → borrar
    autor.delete()
    return JsonResponse({'success': True})