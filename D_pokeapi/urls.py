"""D_pokeapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'lista_pokemons/form/$', listar_pokeapi_form, name='listar_pokeapi_form'),
    url(r'^ver_pokemon/form/(?P<pokemon_id>\d+)/$', detalle_pokeapi_form, name='detalle_pokeapi_form'),
    url(r'lista_pokemons/$', listar_pokeapi, name='listar_pokeapi'),
    url(r'^ver_pokemon/(?P<pokemon_id>\d+)/$', detalle_pokeapi, name='detalle_pokeapi'),
    url(r'^lista_pokemons/tipo/(?P<type_name>[a-z]+)/$', listar_pokeapi_tipo, name='listar_pokeapi_tipo'),
]
