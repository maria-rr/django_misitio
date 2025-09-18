from django.shortcuts import render

#mysite
def inicio(request):
    return render(request, 'inicio.html')  # Renderiza la plantilla inicio.html para el proyecto principal
