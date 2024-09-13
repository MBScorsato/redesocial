from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from plataforma.models import Menssagem_plataforma, OQueTemosParaHoje


@login_required(login_url='/auth/cadastro')  # Redireciona para a página de cadastro se não autenticado
def plataforma(request):
    nome = request.user.username  # Nome do usuário para o contexto

    if request.method == 'GET':
        try:
            # Para o campo "msg_html" (formulário principal)
            msg = Menssagem_plataforma.objects.filter(usuario=request.user).order_by('-id')  # Apenas mensagens do usuário logado
            if msg.exists():  # Verifica se há mensagens
                menssagem = "\n".join(str(item) for item in msg)  # Adiciona as mensagens à variável 'menssagem'
            else:
                menssagem = 'Olá! Estou feliz em conhecer esta plataforma!'  # Se não houver mensagens
        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens: {}'.format(e))
            menssagem = 'Olá! Estou feliz em conhecer esta plataforma!'  # Mensagem padrão

        # Para o campo "msg_html_modal" (formulário do modal)
        try:
            msg_modal = OQueTemosParaHoje.objects.filter(usuario=request.user).order_by('-id')  # Apenas mensagens do modal do usuário logado
            if msg_modal.exists():
                menssagem_modal = "\n".join(str(item) for item in msg_modal)
            else:
                menssagem_modal = 'Ainda não há mensagens para hoje!'  # Caso não haja mensagens no modal
        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens do modal: {}'.format(e))
            menssagem_modal = 'Ainda não há mensagens para hoje!'  # Mensagem padrão para o modal

        return render(request, 'plataforma.html', {'nome': nome, 'menssagem': menssagem, 'menssagem_modal': menssagem_modal})

    if request.method == 'POST':
        # Verifica se é o formulário "msg_html" (formulário principal)
        if 'msg_html' in request.POST:
            nova_mensagem = request.POST.get('msg_html', '').strip()
            if nova_mensagem:
                try:
                    # Filtra as mensagens do usuário conectado
                    msg = Menssagem_plataforma.objects.filter(usuario=request.user).order_by('-id')

                    if msg.exists():  # Verifica se há mensagens
                        # Apaga a última mensagem do usuário logado
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

        # Verifica se é o formulário "msg_html_modal" (formulário do modal)
        elif 'msg_html_modal' in request.POST:

            nova_mensagem_modal = request.POST.get('msg_html_modal', '').strip()

            # Obtém o último registro do usuário, se existir/ tem que ficar fora dos laços para não sobreescrer
            ultimo_registro = OQueTemosParaHoje.objects.filter(usuario=request.user).order_by('-id').first()
            if ultimo_registro:
                contador = ultimo_registro.contador + 1
            else:
                contador = 1

            if nova_mensagem_modal:
                try:
                    # Filtra as mensagens do modal do usuário logado
                    msg_modal = OQueTemosParaHoje.objects.filter(usuario=request.user).order_by('-id')

                    if msg_modal.exists():  # Verifica se há mensagens do modal
                        # Apaga a última mensagem do modal do usuário logado
                        msg_modal.first().delete()

                    # Salva a nova mensagem enviada no modal
                    OQueTemosParaHoje.objects.create(
                        usuario=request.user,
                        msg_hoje=nova_mensagem_modal,
                        contador=contador
                    )
                    menssagem_modal = nova_mensagem_modal  # Exibe a nova mensagem modal na tela

                except Exception as e:
                    messages.error(request, 'Erro ao processar a mensagem do modal: {}'.format(e))
                    menssagem_modal = 'Ainda não há mensagens para hoje!'  # Mensagem padrão para o modal

            else:
                messages.warning(request, 'A mensagem do modal não pode estar vazia.')
            return render(request, 'plataforma.html', {'nome': nome, 'menssagem_modal': menssagem_modal})

    return render(request, 'plataforma.html')


def sair(request):
    auth.logout(request)
    return redirect('/auth/login')
