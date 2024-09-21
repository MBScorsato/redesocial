from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from perfil.models import ImagemPerfil
from django.contrib.auth import update_session_auth_hash


@login_required(login_url='/auth/cadastro')
def perfil(request):
    nome = request.user.username

    if request.method == 'GET':
        # Corrigido para buscar imagens associadas ao usuário logado
        img = ImagemPerfil.objects.filter(usuario=request.user)

        # Captura o email do usuário logado
        email = request.user.email

        return render(request, 'perfil.html', {
            'nome': nome,
            'img': img,  # Passa as imagens do perfil para o template
            'email': email,  # Passa o email do usuário logado para o template
        })

    elif request.method == 'POST':

        # Tratamento da imagem de perfil
        if 'imagem' in request.FILES:
            file = request.FILES.get("imagem")

            # Verifica se o usuário já tem uma imagem de perfil
            try:
                img_existente = ImagemPerfil.objects.get(usuario=request.user)
                # Apaga a imagem anterior
                img_existente.img.delete(save=False)
                img_existente.delete()

            except ImagemPerfil.DoesNotExist:
                pass  # Se não existir imagem, segue com o processo normalmente

            # Salva a nova imagem
            img = ImagemPerfil(usuario=request.user, img=file)
            img.save()

        # Atualiza email e senha
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Verifica se o email foi alterado e se já existe no banco de dados
        if email and email != request.user.email:
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Este email já está em uso.")
                return redirect('perfil')

            else:
                request.user.email = email

        # Verifica se as senhas coincidem e atualiza a senha
        if password1 and password2:
            if password1 == password2:
                request.user.password = make_password(password1)
                request.user.save()

                # Atualiza a hash da sessão para evitar o logout
                update_session_auth_hash(request, request.user)

            else:
                messages.warning(request, "As senhas não coincidem.")
                return redirect('perfil')

        # Salva as mudanças no usuário (email e/ou senha)
        request.user.save()

        # Redireciona para a página de perfil após salvar as alterações
        messages.success(request, "Perfil atualizado com sucesso!")

        return redirect('perfil')


def excluir(request):
    if request.method == 'GET':
        return render(request, 'excluir.html')

    elif request.method == 'POST':
        return render(request, 'excluir.html')


