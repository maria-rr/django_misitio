from django.shortcuts import render

#mapas
def inicio(request):
    return render(request, 'mapas/inicio.html')  # Renderiza la plantilla inicio.html para el proyecto principal
