from django.shortcuts import render

def pantalla_login(request):
    return render(request, 'login.html')

def mapa_granja(request):
    return render(request, 'mapa.html')

def zona_granja(request):
    return render(request, 'granja.html')

def zona_poble(request):
    return render(request, 'placa.html')
