"""
URL configuration for stardew_valley project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.pantalla_login, name='login'), 
    path('mapa/', views.mapa_granja, name='mapa'), 
    path('granja/', views.zona_granja, name='granja'),
    path('poble/', views.zona_poble, name='poble'), 
    path('platja/', views.zona_platja, name='platja'), 
    path('muntanya/', views.zona_muntanya, name='muntanya'),
    path('bosc/', views.zona_bosc, name='bosc'),
    path('perfil/', views.pantalla_perfil, name='perfil'),
    path("pescar/<str:zona>/", views.pescar, name="pescar"),
    path("pescar/<str:zona>/generar/", views.generar_peix, name="generar_peix"),
    path("pescar/<str:zona>/agafar/", views.agafar_peix, name="agafar_peix"),
    path("botiga/llavors/", views.llistar_llavors, name="llistar_llavors"),
    path("botiga/comprar/", views.comprar_llavors, name="comprar_llavors"),
    path('', views.menu_inici, name='inici'),
    path('login/', views.pantalla_login, name='login'),
    path('crear-partida/', views.pantalla_crear_partida, name='crear_partida'),
    path('passar-dia/', views.passar_dia, name='passar_dia'),
    path("crear-partida/", views.pantalla_crear_partida, name="crear_partida"),
]
