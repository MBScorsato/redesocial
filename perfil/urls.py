from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/excluir/', views.excluir, name='excluir'),

]
