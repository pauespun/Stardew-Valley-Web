import os
import django
import random
import itertools
from django.db import transaction

# Configurem l'entorn de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stardew_valley.settings')
django.setup()

from core.models import Usuari, Partida, Article, Inventari

def generar_noms_sensats():
    prefixos = [
        "Fruita", "Flor", "Llavor", "Fulla", "Arrel", "Pocio", "Cristall", 
        "Gemma", "Mineral", "Fusta", "Peix", "Escama", "Ploma", "Ou", 
        "Roca", "Bolet", "Alga", "Cor", "Llagrima", "Pols", "Fragment", 
        "Llibre", "Anell", "Collar", "Reliquia", "Espasa", "Escut", "Casc", 
        "Bota", "Llet", "Formatge", "Iogurt", "Mel", "Vi", "Suc", 
        "Melmelada", "Tela", "Fil", "Barra", "Lingot", "Mena", "Argila", 
        "Esquer", "Geoda", "Artefacte"
    ]
    
    sufixos = [
        "de Foc", "d'Aigua", "de Terra", "de Vent", "de Gel", "de Llum", 
        "d'Ombra", "de Cristall", "de Ferro", "d'Or", "de Plata", "de Coure", 
        "de Fusta", "de Pedra", "de Magia", "de Bosc", "de Muntanya", 
        "de Mar", "de Riu", "de Lluna", "de Sol", "d'Estrella", "del Buit", 
        "del Drac", "de la Fada", "del Mag", "del Rei", "de la Reina", 
        "de Primavera", "d'Estiu", "de Tardor", "d'Hivern", "Radiant", 
        "Lluent", "Antic", "Oblidat", "Perdut", "Secret", "Misterios", 
        "Estrany", "Fresc", "Podrit", "Salat", "Dolc", "Gegant", "Petit", "Mistic"
    ]
    
    combinacions = list(itertools.product(prefixos, sufixos))
    random.shuffle(combinacions)
    
    return [f"{pref} {suf}" for pref, suf in combinacions[:2000]]

def poblar_massiu():
    print("Iniciant la generacio massiva de 2000 articles...")

    # AQUESTA ÉS LA LÍNIA CORREGIDA:
    usuari = Usuari.objects.filter(nom_usuari__iexact="Enric").first()
    if not usuari:
        print("Error: No s'ha trobat cap usuari amb el nom exacte 'enric'.")
        return
        
    partida = Partida.objects.filter(id_usuari=usuari).first()
    if not partida:
        print(f"Error: L'usuari {usuari.nom_usuari} no te cap partida activa.")
        return

    noms_articles = generar_noms_sensats()
    articles_guardats = []
    
    print("1/3 Preparant els 2000 articles...")
    
    print("2/3 Guardant els articles a PostgreSQL (Transaccio Atomica)...")
    with transaction.atomic():
        for nom in noms_articles:
            nou_article = Article.objects.create(
                nom_article=nom,
                preu_venda=random.randint(10, 800),
                qualitat=random.choice(['Normal', 'Plata', 'Or'])
            )
            articles_guardats.append(nou_article)
    
    print("3/3 Omplint l'inventari del teu usuari...")
    nous_items_inventari = []
    
    for article_guardat in articles_guardats:
        nous_items_inventari.append(Inventari(
            quantitat=random.randint(1, 99),
            article=article_guardat,
            partida=partida
        ))
        
    Inventari.objects.bulk_create(nous_items_inventari)
    
    print("-" * 40)
    print(f"EXIT! S'han inserit exactament 2000 articles unics a l'inventari de {usuari.nom_usuari}.")

if __name__ == '__main__':
    poblar_massiu()
