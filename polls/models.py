import datetime

from django.db import models
from django.utils import timezone

class Pregunta(models.Model):
    pregunta_ds = models.CharField(max_length=200)
    publicacion_fh = models.DateTimeField("fecha publicacion")
    def __str__(self):
        return self.pregunta_ds
    def fue_publicada_recientemente(self):
        return self.publicacion_fh >= timezone.now() - datetime.timedelta(days=1)


class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta_ds = models.CharField(max_length= 200)
    votos = models.IntegerField(default=0)
    def __str__(self):
        return self.respuesta_ds

# Create your models here.
