from django import forms
from .models import Pregunta, Respuesta

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['pregunta_ds']

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['pregunta', 'respuesta_ds']