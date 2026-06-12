from django.shortcuts import render

def pantalla_login(request):
    return render(request, 'login.html')

def mapa_granja(request):
    return render(request, 'mapa.html')

def zona_granja(request):
    return render(request, 'granja.html')

def zona_poble(request):
    return render(request, 'placa.html')

def zona_platja(request):
    return render(request, 'platja.html')

def zona_muntanya(request):
    return render(request, 'muntanya.html')

def zona_bosc(request):
    return render(request, 'bosc.html')

def pantalla_perfil(request):
    return render(request, 'perfil.html')
