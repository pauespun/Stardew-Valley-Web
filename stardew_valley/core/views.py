from django.shortcuts import render, redirect
from .models import Partida, EspaiCultiu


# --- PANTALLES BÀSIQUES ---

def menu_inici(request):
    return render(request, 'inici.html')

def pantalla_crear_partida(request):
    return render(request, 'crear_partida.html')

def pantalla_login(request):
    return render(request, 'login.html')

def pantalla_perfil(request):
    return render(request, 'perfil.html')

def mapa_granja(request):
    partida = Partida.objects.first()
    return render(request, 'mapa.html', {'partida': partida})

def passar_dia(request):
    if request.method == 'POST':
        partida = Partida.objects.first()
        if partida:
            partida.dia += 1
            partida.nivell_energia = 270  
            partida.save()
            
            
    return redirect('/mapa')

# --- ZONES DEL JOC ---

def zona_poble(request):
    return render(request, 'placa.html')

def zona_platja(request):
    return render(request, 'platja.html')

def zona_muntanya(request):
    return render(request, 'muntanya.html')

def zona_bosc(request):
    return render(request, 'bosc.html')


# --- ZONA DE LA GRANJA (AMB BASE DE DADES) ---

def zona_granja(request):
    # Agafem la primera partida de la base de dades (com a prova)
    partida = Partida.objects.first()
    
    # Coordenades CSS fixes de les 4 parcel·les
    coordenades = [
        {'top': '28%', 'left': '36%'},
        {'top': '28%', 'left': '65%'},
        {'top': '57%', 'left': '36%'},
        {'top': '57%', 'left': '65%'},
    ]
    
    espais_frontend = []
    
    # Si la partida existeix, busquem els seus espais
    if partida:
        espais_db = EspaiCultiu.objects.filter(partida=partida)
        espais_dict = {espai.numero_parcela: espai for espai in espais_db}
    else:
        espais_dict = {}

    # Construïm les 4 parcel·les de forma segura (tinguin dades a la DB o no)
    for i in range(1, 5):
        espai_real = espais_dict.get(i)
        llavor_plantada = espai_real.llavor if espai_real else None
        
        espais_frontend.append({
            'numero_parcela': i,
            'llavor': llavor_plantada,
            'top': coordenades[i-1]['top'],
            'left': coordenades[i-1]['left'],
        })

    context = {
        'partida': partida,
        'espais': espais_frontend,
    }
    
    return render(request, 'granja.html', context)
