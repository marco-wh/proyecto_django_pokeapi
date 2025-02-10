from django import forms
import requests

poke_api_type = 'https://pokeapi.co/api/v2/type/'

def get_types():
    args = {'limit': 100}
    url = poke_api_type
    response = requests.get(url, params=args)

    if response.status_code == 200:
        payload = response.json()
        results = payload.get("results", [])

        tipos = []
        for tipo in results:
            id = tipo['url'].replace(poke_api_type, '')
            id = id.replace('/', '')

            tipos.append((id, tipo['name']))

        return tipos
    else:
        return []


class TipoForm(forms.Form):
    tipo = forms.ChoiceField(choices=get_types())