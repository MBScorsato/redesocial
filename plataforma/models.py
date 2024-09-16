from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Menssagem_plataforma(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o modelo User
    msg = models.CharField(max_length=105)
    mensagem = models.DateTimeField(default=timezone.now)  # Armazena a data e hora da mensagem

    def __str__(self):
        return self.msg


class OQueTemosParaHoje(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o modelo User
    msg_hoje = models.CharField(max_length=105)
    mensagem = models.DateTimeField(default=timezone.now)  # Armazena a data e hora da mensagem
    contador = models.IntegerField()

    def __str__(self):
        return self.msg_hoje

