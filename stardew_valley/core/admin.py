from django.contrib import admin
from .models import (
    Estacio, Usuari, Partida, Npc, Article, Peix, Cultiu, Plat,
    Llavor, EspaiCultiu, Inventari
)

# --- CONFIGURACIONS OPTIMITZADES PER A L'ADMIN ---

class PartidaAdmin(admin.ModelAdmin):
    raw_id_fields = ('id_usuari',)

class InventariAdmin(admin.ModelAdmin):
    raw_id_fields = ('partida', 'article')

class EspaiCultiuAdmin(admin.ModelAdmin):
    raw_id_fields = ('partida', 'llavor')

# --- NOVES OPTIMITZACIONS (Per evitar menús desplegables infinits d'Articles) ---

class CultiuAdmin(admin.ModelAdmin):
    raw_id_fields = ('id_article',)

class PeixAdmin(admin.ModelAdmin):
    raw_id_fields = ('id_article',)

class PlatAdmin(admin.ModelAdmin):
    raw_id_fields = ('id_article',)

class LlavorAdmin(admin.ModelAdmin):
    raw_id_fields = ('id_article', 'cultiu')


# --- REGISTRE DE TAULES ---

admin.site.register(Estacio)
admin.site.register(Usuari)
admin.site.register(Partida, PartidaAdmin)      
admin.site.register(Npc)
admin.site.register(Article)
admin.site.register(Peix, PeixAdmin)            # Optimitza la càrrega
admin.site.register(Cultiu, CultiuAdmin)        # Optimitza la càrrega
admin.site.register(Plat, PlatAdmin)            # Optimitza la càrrega
admin.site.register(Llavor, LlavorAdmin)        # Optimitza la càrrega
admin.site.register(EspaiCultiu, EspaiCultiuAdmin) 
admin.site.register(Inventari, InventariAdmin)
