from django.shortcuts import render


def galeria(request):

    if request.method == 'GET':
        nome = request.user.username
        return render(request, 'galeria.html', {'nome': nome,

                                                })
    elif request.method == 'POST':
        nome = request.user.username
        return render(request, 'galeria.html', {'nome': nome,

                                                })
