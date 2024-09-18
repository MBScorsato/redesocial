from django.db import models
from django.contrib.auth.models import User


class ImagemPerfil(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona com o modelo User
    img = models.FileField(upload_to="img_perfil")

    def __str__(self):
        return self.usuario.username  # Exibe o nome de usuário no método __str__

