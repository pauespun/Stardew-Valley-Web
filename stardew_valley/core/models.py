from django.db import models
from django.db.models import Q

class Estacio(models.Model):

    class NomEstacio(models.TextChoices):
        PRIMAVERA = "Primavera", "Primavera"
        ESTIU = "Estiu", "Estiu"
        TARDOR = "Tardor", "Tardor"
        HIVERN = "Hivern", "Hivern"

    id_estacio = models.CharField(
        max_length=10,
        primary_key=True
    )

    nom_estacio = models.CharField(
        max_length=10,
        choices=NomEstacio.choices
    )

    class Meta:
        db_table = "estacio"

    def __str__(self):
        return self.nom_estacio

class Usuari(models.Model):
    id_usuari = models.AutoField(primary_key=True)
    nom_usuari = models.CharField(max_length=100)
    email = models.CharField(max_length=150, unique=True)
    
    contrasenya = models.CharField(max_length=255, default="1234")

    class Meta:
        db_table = "usuari"

    def __str__(self):
        return self.nom_usuari

class Partida(models.Model):
    id_partida = models.AutoField(primary_key=True)
    nom_granja = models.CharField(max_length=100)
    nivell_energia = models.IntegerField()
    
    diners = models.IntegerField(default=500)
    
    dia = models.IntegerField(default=1)

    id_usuari = models.ForeignKey(
        "Usuari",
        on_delete=models.CASCADE,
        db_column="id_usuari"
    )

    class Meta:
        db_table = "partida"

    def __str__(self):
        return self.nom_granja

class Npc(models.Model):
    id_npc = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    es_solter = models.BooleanField()
    data_aniversari = models.DateField()

    class Meta:
        db_table = "npc"

    def __str__(self):
        return self.nom

class Article(models.Model):

    class TipusQualitat(models.TextChoices):
        NORMAL = "Normal", "Normal"
        BRONZE = "Bronze", "Bronze"
        PLATA = "Plata", "Plata"
        OR = "Or", "Or"

    id_article = models.AutoField(primary_key=True)
    nom_article = models.CharField(max_length=100)
    preu_venda = models.DecimalField(max_digits=10, decimal_places=2)
    qualitat = models.CharField(max_length=10, choices=TipusQualitat.choices)

    class Meta:
        db_table = "article"

    def __str__(self):
        return self.nom_article

class Peix(models.Model):
    id_article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="id_article"
    )
    ubicacio_pesca = models.CharField(max_length=100)

    class Meta:
        db_table = "peix"

    def __str__(self):
        return self.id_article.nom_article

class Cultiu(models.Model):
    id_article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="id_article"
    )
    temps_creixement = models.IntegerField()

    class Meta:
        db_table = "cultiu"

    def __str__(self):
        return self.id_article.nom_article

class Plat(models.Model):
    id_article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="id_article"
    )
    energia_recuperada = models.IntegerField()

    class Meta:
        db_table = "plat"

    def __str__(self):
        return self.id_article.nom_article

class Llavor(models.Model):
    # CORRECCIÓ: Ara hereta correctament d'Article!
    id_article = models.OneToOneField(
        Article,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="id_article"
    )
    
    preu_compra = models.DecimalField(max_digits=8, decimal_places=2)

    cultiu = models.OneToOneField(
        Cultiu,
        on_delete=models.CASCADE,
        related_name="llavor"
    )
    
    class Meta:
        db_table = "llavor"

class EspaiCultiu(models.Model):
    partida = models.ForeignKey(
        Partida,
        on_delete=models.CASCADE,
        related_name="espais_cultiu"
    )
    numero_parcela = models.PositiveSmallIntegerField()
    
    llavor = models.ForeignKey(
        Llavor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="espais_cultiu"
    )
    
    # NOUS CAMPS: Quantitat plantada i quan es va plantar
    quantitat_plantada = models.IntegerField(default=0)
    data_plantacio = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "espai_cultiu"
        unique_together = ("partida", "numero_parcela")

    def __str__(self):
        return f"Partida {self.partida} - Espai {self.numero_parcela}"

# NOVA TAULA: Inventari
class Inventari(models.Model):
    partida = models.ForeignKey(
        Partida,
        on_delete=models.CASCADE,
        db_column="id_partida"
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        db_column="id_article"
    )
    quantitat = models.IntegerField(default=0)

    class Meta:
        db_table = "inventari"
        unique_together = ("partida", "article")

    def __str__(self):
        return f"Partida {self.partida.id_partida} | Article: {self.article.nom_article} | Qty: {self.quantitat}"


# --- LECTURA DE RESTA DE TAULES (SENSE CANVIS) ---

class Regal(models.Model):
    pk = models.CompositePrimaryKey("id_partida", "id_npc", "id_article", "data_regal")
    id_partida = models.ForeignKey(Partida, on_delete=models.CASCADE, db_column="id_partida")
    id_npc = models.ForeignKey(Npc, on_delete=models.CASCADE, db_column="id_npc")
    id_article = models.ForeignKey(Article, on_delete=models.CASCADE, db_column="id_article")
    data_regal = models.DateField()

    class Meta:
        db_table = "regal"

class Preferencia(models.Model):
    pk = models.CompositePrimaryKey("id_npc", "id_article")

    class TipusReaccio(models.TextChoices):
        AGRADA = "Agrada", "Agrada"
        NEUTRAL = "Neutral", "Neutral"
        ODIA = "Odia", "Odia"

    id_npc = models.ForeignKey(Npc, on_delete=models.CASCADE, db_column="id_npc")
    id_article = models.ForeignKey(Article, on_delete=models.CASCADE, db_column="id_article")
    reaccio = models.CharField(max_length=10, choices=TipusReaccio.choices)

    class Meta:
        db_table = "preferencia"

class EsPesca(models.Model):
    pk = models.CompositePrimaryKey("id_peix", "id_estacio")
    id_peix = models.ForeignKey(Peix, on_delete=models.CASCADE, db_column="id_peix")
    id_estacio = models.ForeignKey(Estacio, on_delete=models.CASCADE, db_column="id_estacio")

    class Meta:
        db_table = "es_pesca"

class CreixEn(models.Model):
    pk = models.CompositePrimaryKey("id_cultiu", "id_estacio")
    id_cultiu = models.ForeignKey(Cultiu, on_delete=models.CASCADE, db_column="id_cultiu")
    id_estacio = models.ForeignKey(Estacio, on_delete=models.CASCADE, db_column="id_estacio")

    class Meta:
        db_table = "creix_en"

class Recepta(models.Model):
    pk = models.CompositePrimaryKey("id_plat", "id_ingredient")
    id_plat = models.ForeignKey(Plat, on_delete=models.CASCADE, db_column="id_plat")
    id_ingredient = models.ForeignKey(Article, on_delete=models.CASCADE, db_column="id_ingredient")
    quantitat_necesaria = models.IntegerField()

    class Meta:
        db_table = "recepta"
        constraints = [
            models.CheckConstraint(
                condition=Q(quantitat_necesaria__gt=0),
                name="recepta_quantitat_necesaria_check"
            )
        ]
