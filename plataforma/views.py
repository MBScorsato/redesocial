from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required



@login_required(login_url='/auth/cadastro')  # Redireciona para a página de cadastro se não autenticado
def plataforma(request):
    nome = request.user  # Captura o nome do usuário logado

    if request.method == 'GET':
        # Renderiza a página com o nome do usuário em uma requisição GET
        return render(request, 'plataforma.html', {'nome': nome})

    elif request.method == 'POST':
        pass
        return render(request, 'plataforma.html', {'nome': nome})


def sair(request):
    auth.logout(request)
    return redirect('/auth/cadastro')

