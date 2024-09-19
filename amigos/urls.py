from django.urls import path
from . import views

urlpatterns = [
    path('amigos/', views.amigos, name='amigos'),

]
