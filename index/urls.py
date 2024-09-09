from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_, name='login'),
    path('recuperar_senha/', views.enviar_email, name='enviar_email'),
]
