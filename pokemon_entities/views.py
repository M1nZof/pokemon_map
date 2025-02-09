import glob

import folium

from django.core.exceptions import ObjectDoesNotExist
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
    time_now = localtime()
    pokemons_entities = PokemonEntity.objects.filter(appeared_at__lt=time_now, disappear_at__gt=time_now)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons_entities:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            request.build_absolute_uri(pokemon.pokemon.image.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    time_now = localtime()
    pokemon = Pokemon.objects.filter(pk=pokemon_id).first()
    pokemons_entities = PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lt=time_now,
                                                     disappear_at__gt=time_now)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.image.url)
        )

    previous_evolution = None
    if pokemon.evolved_from:
        previous_evolution = {
            'title_ru': pokemon.evolved_from.title_ru,
            'pokemon_id': pokemon.evolved_from.pk,
            'img_url': pokemon.evolved_from.image.url
        }

    next_evolution = pokemon.next_evolutions.first()

    if next_evolution:
        next_evolution = {
            "title_ru": next_evolution.title_ru,
            "pokemon_id": next_evolution.pk,
            "img_url": next_evolution.image.url
        }

    pokemon_page = {
        'img_url': pokemon.image.url,
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
