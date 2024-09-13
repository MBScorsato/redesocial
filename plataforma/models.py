from django.contrib.auth.models import User
from django.db import models


class Menssagem_plataforma(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o modelo User
    msg = models.CharField(max_length=105)

    def __str__(self):
        return self.msg


class OQueTemosParaHoje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o modelo User
    msg_hoje = models.CharField(max_length=105)
    data = models.DateField(auto_now_add=True)  # Ou use DateTimeField para data e hora
    contador = models.IntegerField()

    def __str__(self):
        return self.msg_hoje

