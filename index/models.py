from django.db import models


class ImagemIndex(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to="img_index")

    def __str__(self):
        return self.title


class ImagemIndex2(models.Model):
    title2 = models.CharField(max_length=100)
    img2 = models.ImageField(upload_to="img_index")
    contato = models.CharField(max_length=150)

    def __str__(self):
        return self.title2
