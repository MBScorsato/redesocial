from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from perfil.models import ImagemPerfil
from plataforma.models import Menssagem_plataforma, OQueTemosParaHoje


@login_required(login_url='/auth/cadastro')
def plataforma(request):
    nome = request.user.username

    if request.method == 'GET':
        # Tenta buscar as mensagens do usuário na tabela Menssagem_plataforma, ordenando pelo id (do mais recente para o mais antigo)
        try:
            msg = Menssagem_plataforma.objects.filter(usuario=request.user).order_by('-id')

            # Se houver mensagens (verificado com msg.exists()), converte os itens em strings e une com quebras de linha. Caso contrário, define uma mensagem padrão.
            menssagem = "\n".join(
                str(item) for item in msg) if msg.exists() else 'Olá! Estou feliz em conhecer esta plataforma!'

        # Caso ocorra um erro ao buscar as mensagens, captura a exceção e exibe uma mensagem de erro ao usuário.
        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens: {}'.format(e))

            # Se houver erro, define uma mensagem padrão.
            menssagem = 'Olá! Estou feliz em conhecer esta plataforma!'

        # Tenta buscar as mensagens da funcionalidade "OQueTemosParaHoje" para o usuário atual, ordenadas pela
        # mensagem mais recente
        try:
            msg_modal = OQueTemosParaHoje.objects.filter(usuario=request.user).order_by('-mensagem')

            # Se houver mensagens, as converte em strings e une com quebras de linha. Se não, define uma mensagem
            # padrão.
            menssagem_modal = "\n".join(
                str(item) for item in msg_modal) if msg_modal.exists() else 'Ainda não há mensagens para hoje!'

        # Caso ocorra um erro ao buscar as mensagens do modal, captura a exceção e exibe uma mensagem de erro ao
        # usuário.
        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens do modal: {}'.format(e))

            # Se houver erro, define uma mensagem padrão.
            menssagem_modal = 'Ainda não há mensagens para hoje!'

        # Tenta buscar todas as mensagens da funcionalidade "OQueTemosParaHoje", ordenadas pela mensagem mais recente
        try:
            msg_mural = OQueTemosParaHoje.objects.all().order_by('-mensagem')

        # Caso ocorra um erro ao buscar as mensagens do mural, captura a exceção e exibe uma mensagem de erro ao
        # usuário.
        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens do mural: {}'.format(e))

            # Se houver erro, define msg_mural como uma lista vazia.
            msg_mural = []

        # Adiciona a URL da imagem de perfil para cada item em msg_mural
        # Para cada item na lista msg_mural (que contém as mensagens do mural), faz um loop.
        for item in msg_mural:
            # Tenta buscar a imagem de perfil do usuário associado a esse item (mensagem) no modelo ImagemPerfil.
            try:
                img = ImagemPerfil.objects.get(usuario=item.usuario)

                # Se a imagem de perfil for encontrada, atribui o URL da imagem ao atributo imagem_perfil_url do item.
                item.imagem_perfil_url = img.img.url

            # Caso não exista uma imagem de perfil para o usuário (levantando a exceção DoesNotExist), atribui None
            # ao atributo imagem_perfil_url.
            except ImagemPerfil.DoesNotExist:
                item.imagem_perfil_url = None

        imagem_logado = ImagemPerfil.objects.filter(usuario=request.user)
        return render(request, 'plataforma.html', {
            'nome': nome,
            'menssagem': menssagem,
            'menssagem_modal': menssagem_modal,
            'msg_mural': msg_mural,
            'imagem_logado': imagem_logado,

        })

    if request.method == 'POST':
        if 'msg_html_modal' in request.POST:
            nova_mensagem_modal = request.POST.get('msg_html_modal', '').strip()
            msg_banco = OQueTemosParaHoje.objects.filter(usuario=request.user)
            if not msg_banco:
                OQueTemosParaHoje.objects.create(usuario=request.user, msg_hoje='sua mensagem', contador=0)
            if nova_mensagem_modal:
                try:
                    ultimo_registro = OQueTemosParaHoje.objects.filter(usuario=request.user).order_by('-id').first()
                    contador = ultimo_registro.contador + 1 if ultimo_registro else 1
                    OQueTemosParaHoje.objects.filter(usuario=request.user).order_by('-id').first().delete()
                    OQueTemosParaHoje.objects.create(usuario=request.user, msg_hoje=nova_mensagem_modal,
                                                     contador=contador)
                    messages.success(request, 'Salvo com sucesso!')
                except Exception as e:
                    messages.error(request, 'Erro ao processar a mensagem do modal: {}'.format(e))
            else:
                messages.warning(request, 'A mensagem não pode estar vazia.')

        try:
            msg_mural = OQueTemosParaHoje.objects.all().order_by('-mensagem')

            # Adiciona URLs das imagens de perfil aos itens do mural
            for item in msg_mural:
                try:
                    img = ImagemPerfil.objects.get(usuario=item.usuario)
                    item.imagem_perfil_url = img.img.url
                except ImagemPerfil.DoesNotExist:
                    item.imagem_perfil_url = None

            # Pega a imagem de perfil do usuário logado
            imagem_logado = ImagemPerfil.objects.filter(usuario=request.user).first()
            if imagem_logado:
                imagem_logado_url = imagem_logado.img.url
            else:
                imagem_logado_url = None

        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens do mural: {}'.format(e))
            msg_mural = []
            imagem_logado_url = None

        return render(request, 'plataforma.html', {
            'nome': nome,
            'msg_mural': msg_mural,
            'imagem_logado_url': imagem_logado_url,
        })


def sair(request):
    auth.logout(request)
    return redirect('/auth/login')
