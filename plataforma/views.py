from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

from plataforma.models import Menssagem_plataforma


@login_required(login_url='/auth/cadastro')  # Redireciona para a página de cadastro se não autenticado
def plataforma(request):
    nome = request.user  # Captura o nome do usuário logado

    if request.method == 'GET':

        msg = Menssagem_plataforma.objects.all()
        for item in msg:
            menssagem = item
        print(menssagem)

        return render(request, 'plataforma.html', {'nome': nome, 'menssagem': menssagem, })

    elif request.method == 'POST':
        pass
        return render(request, 'plataforma.html', {'nome': nome})


def sair(request):
    auth.logout(request)
    return redirect('/auth/cadastro')

