from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from PIL import Image
from django.contrib import messages
from galeria.models import ImgPublica


@login_required(login_url='/auth/cadastro')
def galeria(request):
    if request.method == 'GET':
        nome = request.user.username
        return render(request, 'galeria.html', {'nome': nome,

                                                })
    elif request.method == 'POST':
        nome = request.user.username
        return render(request, 'galeria.html', {'nome': nome,

                                                })


@login_required(login_url='/auth/cadastro')
def minhas_fotos(request):
    usuario = request.user  # Objeto 'User'

    if request.method == 'GET':
        # Filtrar as imagens do usuário logado e ordenar da mais recente para a mais antiga
        fotos_usuario = ImgPublica.objects.filter(usuario=usuario).order_by('-id')

        return render(request, 'minhas_fotos.html', {'fotos_usuario': fotos_usuario})

    if request.method == 'POST':
        img_publico = request.FILES.get('img_publico')
        descricao = request.POST.get('descricao')

        try:
            # Cria uma instância de ImgPublica associada ao usuário logado
            arquivo = ImgPublica(descricao=descricao, img_pub=img_publico, usuario=usuario)
            arquivo.save()
            messages.success(request, 'Imagem publicada com sucesso!')

        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao tentar publicar a imagem: {e}')

        # Após o POST, recarrega as imagens do usuário na ordem da mais recente para a mais antiga
        fotos_usuario = ImgPublica.objects.filter(usuario=usuario).order_by('-id')
        return render(request, 'minhas_fotos.html', {'fotos_usuario': fotos_usuario})

