from django.contrib.auth.models import User
from django.db import models


class ImgPublica(models.Model):
    descricao = models.TextField()
    img_pub = models.FileField(upload_to="img_publico")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o modelo User

    def __str__(self):
        return self.descricao
