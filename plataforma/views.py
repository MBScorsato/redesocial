from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required

from plataforma.models import Menssagem_plataforma


@login_required(login_url='/auth/cadastro')  # Redireciona para a página de cadastro se não autenticado
def plataforma(request):
    nome = request.user

    if request.method == 'GET':
        try:
            msg = Menssagem_plataforma.objects.filter(usuario=request.user)
            if msg.exists():  # Verifica se há mensagens
                menssagem = ""
                for item in msg:
                    menssagem += str(item) + "\n"  # Adiciona as mensagens à variável 'menssagem'
            else:
                menssagem = 'Ola! Estou feliz em conhecer esta plataforma!'  # Se não houver mensagens
        except:
            print('Não existiu mensagem')
            menssagem = 'Olá! Estou feliz em conhecer esta plataforma!'
        return render(request, 'plataforma.html', {'nome': nome, 'menssagem': menssagem, })

    elif request.method == 'POST':

        return render(request, 'plataforma.html', {'nome': nome})


def sair(request):
    auth.logout(request)
    return redirect('/auth/cadastro')
