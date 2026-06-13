from django.shortcuts import render, redirect
from .models import Usuari, Partida

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

def mapa_granja(request):
    if not request.session.get("id_usuari") or not request.session.get("id_partida"):
        return redirect("login")

    return render(request, "mapa.html")

def zona_granja(request):
    if not request.session.get("id_partida"):
        return redirect("login")

    return render(request, "granja.html")

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
