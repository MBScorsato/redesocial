from django.contrib.auth.models import User
from django.db import models


class Menssagem_plataforma(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o modelo User
    msg = models.CharField(max_length=250)

    def __str__(self):
        return self.msg
