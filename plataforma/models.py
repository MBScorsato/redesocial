from django.db import models


class Menssagem_plataforma(models.Model):  # o que te define
    msg = models.CharField(max_length=250)

    def __str__(self):
        return self.msg
