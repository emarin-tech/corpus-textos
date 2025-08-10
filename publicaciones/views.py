from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from .forms import AutorForm
from .models import Autor
from django.core.paginator import Paginator


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


def crear_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES)
        if form.is_valid():
            autor = form.save(commit=False)
            autor.creado_por = request.user
            autor.modificado_por = request.user
            autor.propietario_usuario = request.user

            # Si tienes un grupo activo asociado al usuario
            if hasattr(request.user, 'grupo_activo'):
                autor.propietario_grupo = request.user.grupo_activo

            autor.save()
            return redirect('publicaciones:autores_inicio')
    else:
        form = AutorForm()

    return render(request, 'publicaciones/autores/crear.html', {'form': form})

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

