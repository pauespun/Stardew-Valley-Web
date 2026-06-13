<<<<<<< HEAD
from django.shortcuts import render
from .models import Partida, EspaiCultiu

# --- PANTALLES BÀSIQUES ---
=======
from django.shortcuts import render, redirect
from .models import Usuari, Partida
>>>>>>> 59f9e78 (views of logig and edit profile)

def pantalla_login(request):
    if request.method == "POST":
        nom_usuari = request.POST.get("usuari")
        nom_granja = request.POST.get("nom_granja")
        contrasenya = request.POST.get("contrasenya")

        partida = Partida.objects.filter(
            nom_granja=nom_granja,
            id_usuari__nom_usuari=nom_usuari,
            id_usuari__contrasenya=contrasenya
        ).select_related("id_usuari").first()

        if partida is None:
            return render(request, "login.html", {
                "error": "Usuari, contrasenya o granja incorrectes"
            })

        request.session["id_usuari"] = partida.id_usuari.id_usuari
        request.session["id_partida"] = partida.id_partida

        return redirect("mapa")

    return render(request, "login.html")

def pantalla_perfil(request):
    return render(request, 'perfil.html')

def mapa_granja(request):
    if not request.session.get("id_usuari") or not request.session.get("id_partida"):
        return redirect("login")

    return render(request, "mapa.html")

<<<<<<< HEAD

# --- ZONES DEL JOC ---
=======
def zona_granja(request):
    if not request.session.get("id_partida"):
        return redirect("login")

    return render(request, "granja.html")
>>>>>>> 59f9e78 (views of logig and edit profile)

def zona_poble(request):
    if not request.session.get("id_partida"):
        return redirect("login")

    return render(request, "placa.html")

def zona_platja(request):
    if not request.session.get("id_partida"):
        return redirect("login")

    return render(request, "platja.html")

def zona_muntanya(request):
    if not request.session.get("id_partida"):
        return redirect("login")

    return render(request, "muntanya.html")

def zona_bosc(request):
    if not request.session.get("id_partida"):
        return redirect("login")

    return render(request, "bosc.html")

<<<<<<< HEAD

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
=======
def pantalla_perfil(request):
    id_usuari = request.session.get("id_usuari")
    id_partida = request.session.get("id_partida")

    if not id_usuari or not id_partida:
        return redirect("login")

    usuari = Usuari.objects.get(id_usuari=id_usuari)
    partida = Partida.objects.get(id_partida=id_partida)

    if request.method == "POST":
        usuari.nom_usuari = request.POST.get("nom_usuari")
        usuari.email = request.POST.get("email")
        partida.nom_granja = request.POST.get("nom_granja")

        usuari.save()
        partida.save()

        return redirect("mapa")

    return render(request, "perfil.html", {
        "usuari": usuari,
        "partida": partida,
    })
>>>>>>> 59f9e78 (views of logig and edit profile)
