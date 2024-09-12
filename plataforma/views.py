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

    if request.method == 'POST':

        if 'msg_html' in request.POST:
            try:
                # Filtra as mensagens do usuário conectado
                msg = Menssagem_plataforma.objects.filter(usuario=request.user).order_by('-id')

                if msg.exists():  # Verifica se há mensagens
                    # Apaga a última mensagem do usuário
                    ultima_mensagem = msg.first()  # Pega a última mensagem (mais recente)
                    ultima_mensagem.delete()

                # Salva a nova mensagem enviada no textarea
                nova_mensagem = request.POST.get('msg_html')
                Menssagem_plataforma.objects.create(usuario=request.user, msg=nova_mensagem)
                menssagem = nova_mensagem  # Exibe a nova mensagem na tela

            except:
                # Se houver um erro, pode exibir uma mensagem padrão
                print('Erro ao processar a mensagem')
                menssagem = 'Olá! Estou feliz em conhecer esta plataforma!'
            return render(request, 'plataforma.html', {'nome': request.user.username, 'menssagem': menssagem})

    return render(request, 'plataforma.html')


def sair(request):
    auth.logout(request)
    return redirect('/auth/cadastro')
