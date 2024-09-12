from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from plataforma.models import Menssagem_plataforma


@login_required(login_url='/auth/cadastro')  # Redireciona para a página de cadastro se não autenticado
def plataforma(request):
    nome = request.user.username  # Nome do usuário para o contexto

    if request.method == 'GET':
        try:
            msg = Menssagem_plataforma.objects.filter(usuario=request.user)
            if msg.exists():  # Verifica se há mensagens
                menssagem = "\n".join(str(item) for item in msg)  # Adiciona as mensagens à variável 'menssagem'
            else:
                menssagem = 'Olá! Estou feliz em conhecer esta plataforma!'  # Se não houver mensagens
        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens: {}'.format(e))
            menssagem = 'Olá! Estou feliz em conhecer esta plataforma!'  # Mensagem padrão
        return render(request, 'plataforma.html', {'nome': nome, 'menssagem': menssagem})

    if request.method == 'POST':
        nova_mensagem = request.POST.get('msg_html', '').strip()
        if nova_mensagem:
            try:
                # Filtra as mensagens do usuário conectado
                msg = Menssagem_plataforma.objects.filter(usuario=request.user).order_by('-id')

                if msg.exists():  # Verifica se há mensagens
                    # Apaga a última mensagem do usuário
                    msg.first().delete()

                # Salva a nova mensagem enviada no textarea
                Menssagem_plataforma.objects.create(usuario=request.user, msg=nova_mensagem)
                menssagem = nova_mensagem  # Exibe a nova mensagem na tela

            except Exception as e:
                messages.error(request, 'Erro ao processar a mensagem: {}'.format(e))
                menssagem = 'Olá! Estou feliz em conhecer esta plataforma!'  # Mensagem padrão

        else:
            messages.warning(request, 'A mensagem não pode estar vazia.')
        return render(request, 'plataforma.html', {'nome': nome, 'menssagem': menssagem})

    return render(request, 'plataforma.html')


def sair(request):
    auth.logout(request)
    return redirect('/auth/login')
