from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
#    path("", views.IndexView.as_view(), name="inicio"),
	path("", views.inicio, name="inicio"),
    path("<int:pregunta_id>/", views.detalle, name="detalle"),
    path("<int:pregunta_id>/resultado/", views.resultado, name="resultado"),
    path("<int:pregunta_id>/votacion/", views.votacion, name="votacion"),
    path("encuesta",views.encuesta, name="encuesta"),
    path("abcEncuesta", views.abcEncuesta, name="abcEncuesta"),

    path('nuevo/', views.nuevo, name='nuevo'),



    path('eliminar/<int:pregunta_id>/', views.eliminar_pregunta, name='eliminar_pregunta'),  # Eliminar una pregunta

    path('eliminar_respuesta/<int:respuesta_id>/', views.eliminar_respuesta, name='eliminar_respuesta'),



    path('listaabc/', views.lista_preguntas, name='lista_preguntas'),  # Mostrar todas las preguntas

    path('editar_pregunta_respuestas/<int:pregunta_id>/', views.editar_pregunta_respuestas, name='editar_pregunta_respuestas'),




]
