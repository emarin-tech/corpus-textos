from django.shortcuts import render

def inicio(request):
    print("🚀 Vista inicio cargada")
    return render(request, 'corpus/inicio.html')