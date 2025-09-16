from django.db.models import F
from django.shortcuts import  HttpResponse,HttpResponseRedirect
#from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice,Question

#def index(request):
#	return HttpResponse("Hello, world. I'm Maria")

def detail(request, question_id):
    #try:
    question = get_object_or_404(Question, pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("La pregunta no existe")
    return render(request, "polls/detail.html",{"question":question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html",{"question":question})

def vote(request, question_id):
    #return HttpResponse("Estas votando la pregunta %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message":"No seleccionaste una opción.",
            },
        )
    else:
        selected_choice.votes=F("votes")+1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)) )



def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


    #V2
    #template = loader.get_template("polls/index.html")
    #context = {
    #    "latest_question_list": latest_question_list,
    #}
    #V1
    #output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(template.render(context, request))

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]


class DatailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model =Question
    template_name = "polls/results.html"


# Create your views here.
