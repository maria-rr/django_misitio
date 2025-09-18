from django.db.models import F
from django.shortcuts import  HttpResponse,HttpResponseRedirect
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Respuesta,Pregunta

#def index(request):
#	return HttpResponse("Hello, world. I'm Maria")

def detail(request, question_id):
    #try:
    question = get_object_or_404(Pregunta, pk=question_id)
    #except Pregunta.DoesNotExist:
    #    raise Http404("La pregunta no existe")
    return render(request, "polls/detail.html",{"pregunta":question})

def results(request, question_id):
    question = get_object_or_404(Pregunta, pk=question_id)
    return render(request, "polls/results.html",{"pregunta":question})

def vote(request, question_id):
    #return HttpResponse("Estas votando la pregunta %s." % question_id)
    question = get_object_or_404(Pregunta, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Respuesta.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "pregunta":question,
                "error_message":"No seleccionaste una opción.",
            },
        )
    else:
        selected_choice.votos= F("votos") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)) )



def index(request):
    latest_question_list = Pregunta.objects.order_by("-publicacion_fh")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


    #V2
    #template = loader.get_template("polls/index.html")
    #context = {
    #    "latest_question_list": latest_question_list,
    #}
    #V1
    #output = ", ".join([q.pregunta_ds for q in latest_question_list])
    return HttpResponse(template.render(context, request))

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Pregunta.objects.order_by("-publicacion_fh")[:5]


class DatailView(generic.DetailView):
    model = Pregunta
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model =Pregunta
    template_name = "polls/results.html"


# Create your views here.
