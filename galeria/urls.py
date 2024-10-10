from django.urls import path
from . import views

urlpatterns = [
    path('galeria/', views.galeria, name='galeria'),

]
