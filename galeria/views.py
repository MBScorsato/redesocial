from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from galeria.models import ImgPublica


# View principal da galeria
@login_required(login_url='/auth/cadastro')
def galeria(request):
    nome = request.user.username
    return render(request, 'galeria.html', {'nome': nome})


# View para visualizar e gerenciar as fotos do usuário logado
@login_required(login_url='/auth/cadastro')
def minhas_fotos(request):
    usuario = request.user  # Objeto 'User'

    if request.method == 'GET':
        # Filtrar as imagens do usuário logado e ordenar da mais recente para a mais antiga
        fotos_usuario = ImgPublica.objects.filter(usuario=usuario).order_by('-id')
        return render(request, 'minhas_fotos.html', {'fotos_usuario': fotos_usuario})

    if request.method == 'POST':
        img_publico = request.FILES.get('img_publico')  # Verifica se uma imagem foi enviada
        descricao = request.POST.get('descricao')

        # Fornece uma descrição padrão caso o usuário não preencha
        if not descricao:
            descricao = 'Minha Foto :)'

        # Verifica se o usuário não selecionou uma imagem
        if not img_publico:
            messages.error(request, 'Por favor, selecione uma imagem para publicar.')
        else:
            try:
                # Cria uma instância de ImgPublica associada ao usuário logado
                arquivo = ImgPublica(descricao=descricao, img_pub=img_publico, usuario=usuario)
                arquivo.save()
                messages.success(request, 'Imagem publicada com sucesso!')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao tentar publicar a imagem: {e}')

        # Recarrega as imagens do usuário na ordem da mais recente para a mais antiga
        fotos_usuario = ImgPublica.objects.filter(usuario=usuario).order_by('-id')
        return render(request, 'minhas_fotos.html', {'fotos_usuario': fotos_usuario})


# View para editar a descrição de uma foto específica
@login_required(login_url='/auth/cadastro')
def editar_foto(request, foto_id):
    # Obter a imagem a ser editada ou retornar 404 se não existir
    foto = get_object_or_404(ImgPublica, id=foto_id, usuario=request.user)

    if request.method == 'POST':
        nova_descricao = request.POST.get('descricao')
        if nova_descricao:
            foto.descricao = nova_descricao
            foto.save()
            messages.success(request, 'Legenda atualizada com sucesso!')
        else:
            messages.error(request, 'A descrição não pode estar vazia.')

        return redirect('minhas_fotos')  # Redireciona para a galeria de fotos do usuário

    return render(request, 'editar_foto.html', {'foto': foto})


# View para excluir uma foto
@login_required(login_url='/auth/cadastro')
def excluir_foto(request, foto_id):
    # Obter a imagem a ser excluída ou retornar 404 se não existir
    foto = get_object_or_404(ImgPublica, id=foto_id, usuario=request.user)

    if request.method == 'POST':
        foto.delete()
        messages.success(request, 'Imagem excluída com sucesso!')
        return redirect('minhas_fotos')

    return render(request, 'minhas_fotos.html')
