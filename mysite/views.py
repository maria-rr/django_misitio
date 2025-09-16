from django.shortcuts import render

#mysite
def index(request):
    return render(request, 'index.html')  # Renderiza la plantilla index.html para el proyecto principal
