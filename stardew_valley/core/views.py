from django.shortcuts import render

def pantalla_login(request):
    return render(request, 'login.html')


def mapa_granja(request):
    return render(request, 'mapa.html')
