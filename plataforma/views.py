from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from perfil.models import ImagemPerfil
from plataforma.models import Menssagem_plataforma, OQueTemosParaHoje


@login_required(login_url='/auth/cadastro')
def plataforma(request):
    nome = request.user.username

    if request.method == 'GET':
        try:
            msg = Menssagem_plataforma.objects.filter(usuario=request.user).order_by('-id')
            menssagem = "\n".join(
                str(item) for item in msg) if msg.exists() else 'Olá! Estou feliz em conhecer esta plataforma!'
        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens: {}'.format(e))
            menssagem = 'Olá! Estou feliz em conhecer esta plataforma!'

        try:
            msg_modal = OQueTemosParaHoje.objects.filter(usuario=request.user).order_by('-mensagem')
            menssagem_modal = "\n".join(
                str(item) for item in msg_modal) if msg_modal.exists() else 'Ainda não há mensagens para hoje!'
        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens do modal: {}'.format(e))
            menssagem_modal = 'Ainda não há mensagens para hoje!'

        try:
            msg_mural = OQueTemosParaHoje.objects.all().order_by('-mensagem')
        except Exception as e:
            messages.error(request, 'Erro ao recuperar mensagens do mural: {}'.format(e))
            msg_mural = []

        # Adiciona a URL da imagem de perfil para cada item em msg_mural
        for item in msg_mural:
            try:
                img = ImagemPerfil.objects.get(usuario=item.usuario)
                item.imagem_perfil_url = img.img.url
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
