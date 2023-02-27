import folium
import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from pogomap.settings import MEDIA_URL
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_entities = PokemonEntity.objects.filter(Q(appeared_at__gt=localtime()) | Q(disappear_at__gt=localtime()))

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons_entities:
        pokemon_image = request.build_absolute_uri(f'{MEDIA_URL}/{pokemon.pokemon.image}')
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            pokemon_image
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemon_image = request.build_absolute_uri(f'{MEDIA_URL}/{pokemon.image}')
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': pokemon_image,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.filter(pk=pokemon_id).first()
    pokemons_entities = PokemonEntity.objects.filter(pokemon=pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        if pokemon_entity.appeared_at > localtime() or pokemon_entity.disappear_at > localtime():
            pokemon_image = request.build_absolute_uri(f'../../{MEDIA_URL}/{pokemon.image}')
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                pokemon_image
            )

    previous_evolution = None
    if pokemon.evolved_from:
        previous_evolution_pokemon_image = request.build_absolute_uri(f'../../{MEDIA_URL}/{pokemon.evolved_from.image}')
        previous_evolution = {
            'title_ru': pokemon.evolved_from.title_ru,
            'pokemon_id': pokemon.evolved_from.pk,
            'img_url': previous_evolution_pokemon_image
        }

    try:
        next_evolution = pokemon.pokemon_evolutions.get()
    except ObjectDoesNotExist:
        next_evolution = None

    if next_evolution:
        next_evolution_pokemon_image = request.build_absolute_uri(f'../../{MEDIA_URL}/{next_evolution.image}')
        next_evolution = {
            "title_ru": next_evolution.title_ru,
            "pokemon_id": next_evolution.pk,
            "img_url": next_evolution_pokemon_image
        }

    pokemon_image = request.build_absolute_uri(f'../../{MEDIA_URL}/{pokemon.image}')
    pokemon_page = {
        'img_url': pokemon_image,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_page,
    })
