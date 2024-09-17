from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/auth/cadastro')
def perfil(request):
    nome = request.user.username
    if request.method == 'GET':
        return render(request, 'perfil.html', {
            'nome': nome,
        })
    elif request.method == 'POST':
        return render(request, 'perfil.html', {
            'nome': nome,
        })
