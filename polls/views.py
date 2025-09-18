from django.db.models import F
from django.shortcuts import  HttpResponse,HttpResponseRedirect
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Respuesta,Pregunta

#def index(request):
#	return HttpResponse("Hello, world. I'm Maria")

def detail(request, pregunta_id):
    #try:
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    #except Pregunta.DoesNotExist:
    #    raise Http404("La pregunta no existe")
    return render(request, "polls/detail.html",{"pregunta":pregunta})

def results(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, "polls/results.html",{"pregunta":pregunta})

def vote(request, pregunta_id):
    #return HttpResponse("Estas votando la pregunta %s." % pregunta_id)
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        pregunta_seleccionada = pregunta.respuesta_set.get(pk=request.POST["respuesta"])
    except (KeyError, Respuesta.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "pregunta":pregunta,
                "error_message":"No seleccionaste una opción.",
            },
        )
    else:
        pregunta_seleccionada.votos= F("votos") + 1
        pregunta_seleccionada.save()

        return HttpResponseRedirect(reverse("polls:results",args=(pregunta.id,)) )



def index(request):
    preguntas_recientes_lista = Pregunta.objects.order_by("-publicacion_fh")[:5]
    contexto = {"preguntas_recientes_lista": preguntas_recientes_lista}
    return render(request, "polls/index.html", contexto)


    #V2
    #template = loader.get_template("polls/index.html")
    #context = {
    #    "preguntas_recientes_lista": preguntas_recientes_lista,
    #}
    #V1
    #output = ", ".join([q.pregunta_ds for q in preguntas_recientes_lista])
    return HttpResponse(template.render(context, request))

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "preguntas_recientes_lista"

    def get_queryset(self):
        return Pregunta.objects.order_by("-publicacion_fh")[:5]


class DatailView(generic.DetailView):
    model = Pregunta
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model =Pregunta
    template_name = "polls/results.html"


# Create your views here.
