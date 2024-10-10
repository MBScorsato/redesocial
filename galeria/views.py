from django.shortcuts import render


def galeria(request):
    if request.method == 'GET':
        return render(request, 'galeria.html')
    elif request.method == 'POST':
        return render(request, 'galeria.html')
