from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.plataforma, name='plataforma'),
    path('sair/', views.sair, name="sair"),

]
