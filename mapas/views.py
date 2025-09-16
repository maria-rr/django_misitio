from django.shortcuts import render

#mapas
def index(request):
    return render(request, 'mapas/index.html')  # Renderiza la plantilla index.html para el proyecto principal
