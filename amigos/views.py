from django.contrib.auth.models import User
from django.shortcuts import render
from perfil.models import ImagemPerfil
from django.db.models import Q


def amigos(request):
    nome = request.user.username
    usuarios = User.objects.all()

    # Obter todas as imagens de perfil relacionadas aos usuários
    usuarios_com_imagem = []

    for usuario in usuarios:
        try:
            imagem_perfil = ImagemPerfil.objects.get(usuario=usuario)
        except ImagemPerfil.DoesNotExist:
            imagem_perfil = None  # Caso o usuário não tenha imagem de perfil

        usuarios_com_imagem.append({
            'usuario': usuario,
            'imagem': imagem_perfil
        })

    if request.method == 'GET':
        return render(request, 'amigos.html', {
            'nome': nome,
            'usuarios_com_imagem': usuarios_com_imagem,
        })

    elif request.method == 'POST':

        search_query = request.POST.get('search')

        # Filtra os usuários pelo nome de usuário
        if search_query:
            usuarios = User.objects.filter(Q(username__icontains=search_query))
        else:
            usuarios = User.objects.all()

        # Monta a lista de usuários com suas respectivas imagens
        usuarios_com_imagem = []

        for usuario in usuarios:
            try:
                imagem = ImagemPerfil.objects.get(usuario=usuario)
            except ImagemPerfil.DoesNotExist:
                imagem = None
            usuarios_com_imagem.append({'usuario': usuario, 'imagem': imagem})

        return render(request, 'amigos.html', {
            'nome': request.user.username,
            'usuarios_com_imagem': usuarios_com_imagem,

        })

