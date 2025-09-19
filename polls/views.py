from django.db.models import F
from django.shortcuts import  HttpResponse,HttpResponseRedirect
#from django.http import Http404
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import JsonResponse
from .models import Respuesta,Pregunta
from .forms import PreguntaForm, RespuestaForm


def inicio(request):
    return render(request, 'polls/inicio.html')

def abcEncuesta(request):
    return render(request, 'polls/abcEncuesta.html')




def detalle(request, pregunta_id):
    #try:
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    #except Pregunta.DoesNotExist:
    #    raise Http404("La pregunta no existe")
    return render(request, "polls/detalle.html",{"pregunta":pregunta})

def resultado(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, "polls/resultado.html",{"pregunta":pregunta})

def votacion(request, pregunta_id):
    #return HttpResponse("Estas votando la pregunta %s." % pregunta_id)
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        pregunta_seleccionada = pregunta.respuesta_set.get(pk=request.POST["respuesta"])
    except (KeyError, Respuesta.DoesNotExist):
        return render(
            request,
            "polls/detalle.html",
            {
                "pregunta":pregunta,
                "error_message":"No seleccionaste una opción.",
            },
        )
    else:
        pregunta_seleccionada.votos= F("votos") + 1
        pregunta_seleccionada.save()

        return HttpResponseRedirect(reverse("polls:resultado",args=(pregunta.id,)) )


def encuesta(request):
    preguntas_recientes_lista = Pregunta.objects.order_by("-publicacion_fh")[:5]


    # Capturamos el parámetro 'mostrar_boton' de la URL
    contestar_encuesta = request.GET.get('contestar_encuesta', 'false') == 'true'  # Esto asegurará que sea booleano True o False

    # Pasamos 'mostrar_boton' al contexto
    contexto = {
        "preguntas_recientes_lista": preguntas_recientes_lista,
        "contestar_encuesta": contestar_encuesta  # Agregamos el valor al contexto
    }


    return render(request, "polls/encuesta.html", contexto)


#class IndexView(generic.ListView):
#    template_name = "polls/inicio.html"
#    context_object_name = "preguntas_recientes_lista"

#    def get_queryset(self):
#        return Pregunta.objects.order_by("-publicacion_fh")[:5]


class DetailView(generic.DetailView):
    template_name = "polls/inicio.html"
    context_object_name = "preguntas_recientes_lista"

    def get_queryset(self):
        return Pregunta.objects.order_by("-publicacion_fh")[:5]

#class DetailView(generic.DetailView):
#    model = Pregunta
#    template_name = "polls/detalle.html"


#class ResultsView(generic.DetailView):
#    model =Pregunta
#    template_name = "polls/resultado.html"


# Create your views here.


################################# ABC - CRUD


# Vista para mostrar todas las preguntas
def lista_preguntas(request):
    preguntas = Pregunta.objects.all()
    return render(request, 'polls/lista_preguntas.html', {'preguntas': preguntas})



# Vista para eliminar una pregunta
def eliminar_pregunta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    if request.method == 'POST':
        pregunta.delete()
        return redirect('polls:lista_preguntas')
    return render(request, 'polls/eliminar_pregunta.html', {'pregunta': pregunta})


# Vista para eliminar una respuesta
def eliminar_respuesta(request, respuesta_id):
    respuesta = get_object_or_404(Respuesta, pk=respuesta_id)
    pregunta_id = respuesta.pregunta.id
    if request.method == 'POST':
        respuesta.delete()
        return redirect('polls:detalle_pregunta', pregunta_id=pregunta_id)
    return render(request, 'polls/eliminar_respuesta.html', {'respuesta': respuesta})





def nuevo(request):
    if request.method == 'POST':
        # Capturamos la pregunta
        pregunta_ds = request.POST.get('pregunta_ds')

        # Creamos la pregunta
        pregunta = Pregunta.objects.create(pregunta_ds=pregunta_ds, publicacion_fh=timezone.now())

        # Capturamos todas las respuestas y las guardamos
        respuestas = request.POST.getlist('respuesta_ds')  # Esto captura todas las respuestas

        for respuesta_text in respuestas:
            Respuesta.objects.create(pregunta=pregunta, respuesta_ds=respuesta_text)

        return redirect('polls:lista_preguntas')  # O la URL donde desees redirigir después

    return render(request, 'polls/nuevo.html')

def editar_pregunta_respuestas(request, pregunta_id):
    # Obtener la pregunta y sus respuestas relacionadas
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    respuestas = Respuesta.objects.filter(pregunta=pregunta)

    if request.method == 'POST':
        # Guardar la pregunta
        form = PreguntaForm(request.POST, instance=pregunta)
        if form.is_valid():
            pregunta = form.save()

            # Procesar las respuestas
            respuestas_recibidas = request.POST.getlist('respuesta_ds')  # Obtenemos todas las respuestas
            for idx, respuesta_text in enumerate(respuestas_recibidas):
                if respuesta_text:  # Solo procesamos respuestas no vacías
                    if idx < len(respuestas):
                        # Actualizamos las respuestas existentes
                        respuestas[idx].respuesta_ds = respuesta_text
                        respuestas[idx].save()
                    else:
                        # Creamos nuevas respuestas si hay más de las existentes
                        Respuesta.objects.create(pregunta=pregunta, respuesta_ds=respuesta_text)
            return redirect('polls:lista_preguntas')  # Redirige a la lista de preguntas después de editar
    else:
        form = PreguntaForm(instance=pregunta)

    return render(request, 'polls/editar_pregunta_respuestas.html', {'form': form, 'pregunta': pregunta, 'respuestas': respuestas})

