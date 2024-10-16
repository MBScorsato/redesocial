from django.urls import path
from . import views

urlpatterns = [
    path('galeria/', views.galeria, name='galeria'),
    path('galeria/minhas_fotos', views.minhas_fotos, name='minhas_fotos'),

]
