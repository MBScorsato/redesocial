from django.shortcuts import render

def amigos(request):
    nome = request.user.username
    if request.method == 'GET':
        return render(request, 'amigos.html', {'nome': nome})  # Corrigido para ser um dicionário
    elif request.method == 'POST':
        return render(request, 'amigos.html')

