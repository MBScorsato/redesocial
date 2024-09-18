from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from perfil.models import ImagemPerfil


@login_required(login_url='/auth/cadastro')
def perfil(request):
    nome = request.user.username

    if request.method == 'GET':
        # Corrigido para buscar imagens associadas ao usuário logado
        img = ImagemPerfil.objects.filter(usuario=request.user)

        return render(request, 'perfil.html', {
            'nome': nome,
            'img': img,  # Passa as imagens do perfil para o template
        })

    elif request.method == 'POST':

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

    # Redireciona para a mesma página após salvar a imagem
    return redirect('perfil')
