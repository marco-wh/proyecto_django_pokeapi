from django.shortcuts import render, redirect
import json, requests
from .forms import *

poke_api_gen = 'https://pokeapi.co/api/v2/pokemon-form/'
poke_api_pok = 'https://pokeapi.co/api/v2/pokemon/'
poke_api_version = 'https://pokeapi.co/api/v2/version-group/'
poke_api_type = 'https://pokeapi.co/api/v2/type/'


def index(request):
    return render(request, 'index.html')


def listar_pokeapi_form(request):
    if request.method == 'GET':
        get_offset = int(request.GET.get('offset', 0))
        if get_offset <= 0:
            offset = 0
        else:
            offset = get_offset % 1527

        get_limit = int(request.GET.get('limit', 10))
        if get_limit <= 0 :
            limit = 10
        else:
            limit = get_limit % 1527
    else:
        offset = 0
        limit = 10

    lista = get_pokemons(poke_api_gen, offset=offset, limit=limit)
    count, next, previous = get_nav(offset=offset, limit=limit)

    for pokemon in lista:
        info = get_pokemon(pokemon['url'],
                               claves=['id', 'order', 'sprites', 'types', 'version_group', 'names', 'form_names'])

        pokemon['sprite'] = info['sprites']['front_default']
        pokemon['versions'] = [info['version_group']['name']]
        pokemon['order'] = info['order']
        pokemon['id'] = info['id']
        pokemon['types'] = []
        for type in info['types']:
            pokemon['types'].append(type['type']['name'])

        if not info['names'] == []:
            for n in info['names']:
                if n['language']['name'] == 'en':
                    pokemon['name'] = n['name']
                    break

        pokemon['name'] = pokemon['name'].replace('-', ' ')

    context = {'pokemons': lista,
               'offset': offset,
               'limit': limit,
               'count': count,
               'next': next,
               'previous': previous
               }

    return render(request, 'pokemon/listar_pokemons_form.html', context)


def detalle_pokeapi_form(request, pokemon_id):
    pokemon = get_pokemon(poke_api_gen + pokemon_id)
    if not pokemon['names'] == []:
        for n in pokemon['names']:
            if n['language']['name'] == 'en':
                pokemon['name'] = n['name']
                break

    pokemon['abilities'] = []
    pokemon['origin'] = {}
    pokemon['moves'] = []
    pokemon2 = get_pokemon(pokemon['pokemon']['url'])

    for a in pokemon2['abilities']:
        pokemon['abilities'].append(a['ability']['name'])

    for m in pokemon2['moves']:
        pokemon['moves'].append(m['move']['name'])

    id_pokemon = pokemon['pokemon']['url'].replace(poke_api_pok, '')
    id_pokemon = id_pokemon.replace('/', '')
    pokemon['origin']['id'] = id_pokemon
    pokemon['origin']['name'] = pokemon['pokemon']['name']


    context = {'pokemon': pokemon}
    return render(request, 'pokemon/ver_pokemon_form.html', context)


def listar_pokeapi(request):
    if request.method == 'GET':
        get_offset = int(request.GET.get('offset', 0))
        if get_offset <= 0:
            offset = 0
        else:
            offset = get_offset % 1304

        get_limit = int(request.GET.get('limit', 10))
        if get_limit <= 0 :
            limit = 10
        else:
            limit = get_limit % 1304
    else:
        offset = 0
        limit = 10

    lista = get_pokemons(poke_api_pok, offset=offset, limit=limit)
    count, next, previous = get_nav(offset=offset, limit=limit)

    for pokemon in lista:
        info = get_pokemon(pokemon['url'],
                               claves=['id', 'sprites', 'types', 'game_indices', 'names'])

        pokemon['sprite'] = info['sprites']['front_default']
        pokemon['id'] = info['id']
        pokemon['types'] = []
        pokemon['types_id'] = []
        for type in info['types']:
            pokemon['types'].append(type['type']['name'])

            id = type['type']['url'].replace(poke_api_type, '')
            id = id.replace('/', '')
            pokemon['types_id'].append(id)


        pokemon['versions'] = []
        for version in info['game_indices']:
            pokemon['versions'].append(version['version']['name'])

        pokemon['name'] = pokemon['name'].replace('-', ' ')

    context = {'pokemons': lista,
               'offset': offset,
               'limit': limit,
               'count': count,
               'next': next,
               'previous': previous,
               }

    return render(request, 'pokemon/listar_pokemons.html', context)


def detalle_pokeapi(request, pokemon_id):
    pokemon = get_pokemon(poke_api_pok + pokemon_id)

    pokemon['abilities_'] = []
    pokemon['forms_'] = []
    pokemon['moves_'] = []
    pokemon['versions_'] = []

    for a in pokemon['abilities']:
        pokemon['abilities_'].append(a['ability']['name'])

    for m in pokemon['moves']:
        pokemon['moves_'].append(m['move']['name'])

    for v in pokemon['game_indices']:
        pokemon['versions_'].append(v['version']['name'])

    for f in pokemon['forms']:
        if f['name'] != pokemon['name']:
            id = f['url'].replace(poke_api_gen, '')
            id = id.replace('/', '')

            pokemon['forms_'].append({'id': id, 'name':f['name'].replace('-', ' ')})

    pokemon['name'] = pokemon['name'].replace('-', ' ')

    context = {'pokemon': pokemon}
    return render(request, 'pokemon/ver_pokemon.html', context)


def listar_pokeapi_tipo(request, type_name):
    if request.method == 'GET':
        get_offset = int(request.GET.get('offset', 0))
        if get_offset <= 0:
            offset = 0
        else:
            offset = get_offset

        get_limit = int(request.GET.get('limit', 10))
        if get_limit <= 0:
            limit = 10
        else:
            limit = get_limit
    else:
        offset = 0
        limit = 10

    lista = get_pokemons_types(type_name)
    pokemons = []

    next = False
    previous = False

    if offset + limit >= len(lista):
        upset = len(lista)
    else:
        upset = offset + limit

    for i in range(offset, upset):
        pokemon = lista[i]

        info = get_pokemon(pokemon['pokemon']['url'],
                               claves=['id', 'sprites', 'types', 'game_indices', 'name'])

        pokemon['id'] = info['id']
        pokemon['types'] = []
        pokemon['name'] = info['name'].replace('-', ' ')
        pokemon['versions'] = []
        for type in info['types']:
            pokemon['types'].append(type['type']['name'])

        pokemon['versions'] = []
        for version in info['game_indices']:
            pokemon['versions'].append(version['version']['name'])

        if info['sprites']['front_default']:
            pokemon['sprite'] = info['sprites']['front_default']
        elif info['sprites']['other']:
            pokemon['sprite'] = info['sprites']['other']['home']['front_default']
        pokemons.append(pokemon)

    if (offset > 0) or (offset - limit > 0):
        previous = True

    if (offset + limit < len(lista)):
        next = True

    context = {'pokemons': pokemons,
               'offset': offset,
               'limit': limit,
               'count': len(lista),
               'next': next,
               'previous': previous,
               'l_type': type_name,
               }


    return render(request, 'pokemon/listar_pokemons.html', context)


#------------------------------------------------------------------------
# region Pokemons
def get_nav(url=poke_api_gen, offset=0, limit=20):
    args = {'offset': offset, 'limit': limit}
    response = requests.get(url, params=args)
    if response.status_code == 200:
        payload = response.json()
        return payload.get('count', 0), payload.get('next', ''), payload.get('previous', '')
    else:
        return []


def get_pokemons(url, offset=0, limit=0):
    args = {'offset': offset, 'limit': limit}
    response = requests.get(url, params=args)

    if response.status_code == 200:
        payload = response.json()
        results = payload.get("results", [])
        return results
    else:
        return []


def get_pokemon(url, claves=[]):
    response = requests.get(url)

    if response.status_code == 200:
        payload = response.json()
        if claves:
            results = {}
            for c in claves:
                results[c] = payload.get(c, [])
        else:
            results = payload
        return results
    else:
        return []


def get_pokemons_types(type_name):
    url = poke_api_type + type_name
    response = requests.get(url)

    if response.status_code == 200:
        payload = response.json()
        results = payload.get("pokemon", [])
        return results
    else:
        return []


# endregion Pokemons
