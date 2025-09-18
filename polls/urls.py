from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="inicio"),
	path("", views.inicio, name="inicio"),
    path("<int:pregunta_id>/", views.detalle, name="detalle"),
    path("<int:pregunta_id>/resultado/", views.resultado, name="resultado"),
    path("<int:pregunta_id>/votacion/", views.votacion, name="votacion"),
]
