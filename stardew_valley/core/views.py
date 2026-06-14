import random
import json
from datetime import date
from django.views.decorators.http import require_GET, require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Usuari, Partida, EspaiCultiu, Peix, EsPesca, Inventari, Llavor, Npc, Regal, Preferencia


# --- PANTALLES BÀSIQUES ---

def menu_inici(request):
    return render(request, 'inici.html')
    
def tancar_sessio(request):

    request.session.flush()

    return redirect('/')

def pantalla_crear_partida(request):
    if request.method == "POST":
        nom_usuari = request.POST.get("nom_usuari")
        email = request.POST.get("email_usuari")
        contrasenya = request.POST.get("contrasenya")
        nom_granja = request.POST.get("nom_granja")

        try:
            usuari = Usuari.objects.get(
                nom_usuari=nom_usuari,
                email=email,
                contrasenya=contrasenya
            )
        except Usuari.DoesNotExist:
            return render(request, "crear_partida.html", {
                "error": "L'usuari no existeix o les dades no són correctes"
            })

        partida = Partida.objects.create(
            nom_granja=nom_granja,
            nivell_energia=270,
            diners=500,
            dia=1,
            estacio_actual_id="PRIM",
            id_usuari=usuari
        )

        request.session["id_usuari"] = usuari.id_usuari
        request.session["id_partida"] = partida.id_partida

        return redirect("mapa")

    return render(request, "crear_partida.html")

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
    partida = obtenir_partida_actual(request)
    if not partida:
        return redirect("login")

    inventari = Inventari.objects.filter(partida=partida, quantitat__gt=0).select_related('article')

    return render(request, "mapa.html", {"partida": partida, "inventari": inventari})

def passar_dia(request):
    if request.method == 'POST':
        partida = Partida.objects.first()
        if partida:
            partida.dia += 1
            partida.nivell_energia = 270  
            partida.save()
            
            
    return redirect('/mapa')

# --- ZONES DEL JOC ---
def zona_granja(request):
    partida = obtenir_partida_actual(request)
    if not partida:
        return redirect("login")

    return render(request, "granja.html", {"partida": partida})

def zona_poble(request):
    partida = obtenir_partida_actual(request)
    if not partida:
        return redirect("login")

    return render(request, "placa.html", {"partida": partida})

def zona_platja(request):
    partida = obtenir_partida_actual(request)
    if not partida:
        return redirect("login")

    return render(request, "platja.html", {"partida": partida})

def zona_muntanya(request):
    partida = obtenir_partida_actual(request)
    if not partida:
        return redirect("login")

    return render(request, "muntanya.html", {"partida": partida})

def zona_bosc(request):
    partida = obtenir_partida_actual(request)
    if not partida:
        return redirect("login")

    return render(request, "bosc.html", {"partida": partida})

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

def pescar(request, zona):
    id_partida = request.session.get("id_partida")

    if not id_partida:
        return redirect("login")

    partida = Partida.objects.get(id_partida=id_partida)

    if partida.nivell_energia < 10:
        return redirect(zona.lower())

    relacions = EsPesca.objects.filter(
        id_estacio=partida.estacio_actual,
        id_peix__ubicacio_pesca=zona
    )

    if not relacions.exists():
        return redirect(zona.lower())

    relacio = random.choice(list(relacions))
    peix = relacio.id_peix

    item, creat = Inventari.objects.get_or_create(
        partida=partida,
        article=peix.id_article,
        defaults={"quantitat": 0}
    )

    item.quantitat += 1
    item.save()

    partida.nivell_energia -= 10
    partida.save()

    return redirect(zona.lower())

def generar_peix(request, zona):
    id_partida = request.session.get("id_partida")

    if not id_partida:
        return JsonResponse({"error": "No hi ha sessió"}, status=403)

    partida = Partida.objects.get(id_partida=id_partida)

    if partida.nivell_energia < 10:
        return JsonResponse({"error": "No tens prou energia"}, status=400)

    relacions = EsPesca.objects.filter(
        id_estacio=partida.estacio_actual,
        id_peix__ubicacio_pesca=zona
    )

    if not relacions.exists():
        return JsonResponse({"error": "No hi ha peixos disponibles"}, status=404)

    relacio = random.choice(list(relacions))
    peix = relacio.id_peix
    article = peix.id_article

    request.session["peix_capturat_id"] = article.id_article

    return JsonResponse({
        "nom": article.nom_article,
        "qualitat": article.qualitat,
    })


def agafar_peix(request, zona):
    if request.method != "POST":
        return JsonResponse({"error": "Mètode no permès"}, status=405)

    id_partida = request.session.get("id_partida")
    id_article = request.session.get("peix_capturat_id")

    if not id_partida or not id_article:
        return JsonResponse({"error": "No hi ha captura pendent"}, status=400)

    partida = Partida.objects.get(id_partida=id_partida)

    item, created = Inventari.objects.get_or_create(
        partida=partida,
        article_id=id_article,
        defaults={"quantitat": 0}
    )

    item.quantitat += 1
    item.save()

    partida.nivell_energia -= 10
    partida.save()

    del request.session["peix_capturat_id"]

    return JsonResponse({
        "ok": True,
        "energia": partida.nivell_energia,
        "quantitat": item.quantitat,
    })

@require_GET
def llistar_llavors(request):
    if not request.session.get("id_partida"):
        return JsonResponse({"error": "No hi ha sessió"}, status=403)

    llavors = Llavor.objects.select_related("id_article").all()

    dades = []
    for llavor in llavors:
        dades.append({
            "id": llavor.id_article.id_article,
            "nom": llavor.id_article.nom_article,
            "preu": float(llavor.preu_compra),
        })

    return JsonResponse({"llavors": dades})


@require_POST
def comprar_llavors(request):
    id_partida = request.session.get("id_partida")

    if not id_partida:
        return JsonResponse({"error": "No hi ha sessió"}, status=403)

    partida = Partida.objects.get(id_partida=id_partida)
    dades = json.loads(request.body)

    cistella = dades.get("cistella", {})

    total = 0
    compres = []

    for id_article, quantitat in cistella.items():
        quantitat = int(quantitat)

        if quantitat <= 0:
            continue

        llavor = Llavor.objects.get(id_article_id=id_article)
        subtotal = llavor.preu_compra * quantitat

        total += subtotal
        compres.append((llavor, quantitat))

    if partida.diners < total:
        return JsonResponse({
            "error": "No tens prou diners"
        }, status=400)

    for llavor, quantitat in compres:
        item, created = Inventari.objects.get_or_create(
            partida=partida,
            article=llavor.id_article,
            defaults={"quantitat": 0}
        )

        item.quantitat += quantitat
        item.save()

    partida.diners -= int(total)
    partida.save()

    return JsonResponse({
        "ok": True,
        "diners": partida.diners
    })

def obtenir_partida_actual(request):
    id_partida = request.session.get("id_partida")

    if not id_partida:
        return None

    return Partida.objects.get(id_partida=id_partida)

@require_GET
def llistar_inventari_venda(request):
    id_partida = request.session.get("id_partida")

    if not id_partida:
        return JsonResponse({"error": "No hi ha sessió"}, status=403)

    inventari = Inventari.objects.filter(
        partida_id=id_partida,
        quantitat__gt=0
    ).select_related("article")

    articles = []

    for item in inventari:
        articles.append({
            "id": item.article.id_article,
            "nom": item.article.nom_article,
            "preu": float(item.article.preu_venda),
            "estoc": item.quantitat,
        })

    return JsonResponse({"articles": articles})


@require_POST
def vendre_articles(request):
    id_partida = request.session.get("id_partida")

    if not id_partida:
        return JsonResponse({"error": "No hi ha sessió"}, status=403)

    partida = Partida.objects.get(id_partida=id_partida)
    dades = json.loads(request.body)
    cistella = dades.get("cistella", {})

    total = 0
    vendes = []

    for id_article, quantitat in cistella.items():
        quantitat = int(quantitat)

        if quantitat <= 0:
            continue

        try:
            item = Inventari.objects.select_related("article").get(
                partida=partida,
                article_id=id_article
            )
        except Inventari.DoesNotExist:
            return JsonResponse({
                "error": "Aquest article no existeix al teu inventari"
            }, status=400)

        if quantitat > item.quantitat:
            return JsonResponse({
                "error": f"No tens prou quantitat de {item.article.nom_article}"
            }, status=400)

        subtotal = item.article.preu_venda * quantitat
        total += subtotal
        vendes.append((item, quantitat))

    for item, quantitat in vendes:
        item.quantitat -= quantitat

        if item.quantitat <= 0:
            item.delete()
        else:
            item.save()

    partida.diners += int(total)
    partida.save()

    return JsonResponse({
        "ok": True,
        "diners": partida.diners
    })

@require_GET
def llistar_npcs(request):
    if not request.session.get("id_partida"):
        return JsonResponse({"error": "No hi ha sessió"}, status=403)

    id_partida = request.session["id_partida"]
    clau_sessio = f"npc_inici_partida_{id_partida}"

    ultim_npc = Npc.objects.order_by("-id_npc").first()

    if not ultim_npc:
        return JsonResponse({"npcs": []})

    max_id = ultim_npc.id_npc

    if max_id <= 30:
        inici = 1
    else:
        if clau_sessio not in request.session:
            request.session[clau_sessio] = random.randint(1, max_id - 30)

        inici = request.session[clau_sessio]

    npcs = Npc.objects.filter(
        id_npc__gte=inici
    ).order_by("id_npc")[:30]

    dades = []

    for npc in npcs:
        dades.append({
            "id": npc.id_npc,
            "nom": npc.nom,
            "aniversari": npc.data_aniversari.strftime("%d/%m"),
        })

    return JsonResponse({"npcs": dades})


@require_GET
def llistar_inventari_regal(request):
    id_partida = request.session.get("id_partida")

    if not id_partida:
        return JsonResponse({"error": "No hi ha sessió"}, status=403)

    inventari = Inventari.objects.filter(
        partida_id=id_partida,
        quantitat__gt=0
    ).select_related("article").order_by("article__nom_article")

    articles = []
    for item in inventari:
        articles.append({
            "id": item.article.id_article,
            "nom": item.article.nom_article,
            "quantitat": item.quantitat,
        })

    return JsonResponse({"articles": articles})


@require_POST
def regalar_article(request):
    id_partida = request.session.get("id_partida")

    if not id_partida:
        return JsonResponse({"error": "No hi ha sessió"}, status=403)

    dades = json.loads(request.body)
    id_npc = dades.get("id_npc")
    id_article = dades.get("id_article")

    partida = Partida.objects.get(id_partida=id_partida)

    try:
        item = Inventari.objects.get(
            partida=partida,
            article_id=id_article
        )
    except Inventari.DoesNotExist:
        return JsonResponse({"error": "No tens aquest article"}, status=400)

    if item.quantitat <= 0:
        return JsonResponse({"error": "No tens prou quantitat"}, status=400)

    item.quantitat -= 1

    if item.quantitat <= 0:
        item.delete()
    else:
        item.save()

    Regal.objects.create(
        id_partida=partida,
        id_npc_id=id_npc,
        id_article_id=id_article,
        data_regal=date.today()
    )

    preferencia = Preferencia.objects.filter(
        id_npc_id=id_npc,
        id_article_id=id_article
    ).first()

    if preferencia:
        reaccio = preferencia.reaccio
    else:
        reaccio = "Neutral"

    return JsonResponse({
        "ok": True,
        "reaccio": reaccio
    })