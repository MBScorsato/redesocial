from django.urls import path
from . import views

urlpatterns = [
    path('galeria/', views.galeria, name='galeria'),
    path('galeria/minhas_fotos/', views.minhas_fotos, name='minhas_fotos'),
    path('galeria/editar_foto/<int:foto_id>/', views.editar_foto, name='editar_foto'),
    path('galeria/excluir_foto/<int:foto_id>/', views.excluir_foto, name='excluir_foto'),
]
