from django.contrib.auth.models import User
from django.shortcuts import render
from perfil.models import ImagemPerfil


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
        return render(request, 'amigos.html', {
            'nome': nome,
            'usuarios_com_imagem': usuarios_com_imagem,
        })
