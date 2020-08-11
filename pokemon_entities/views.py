import folium
from pokemon_entities.models import Pokemon, PokemonEntity
from django.shortcuts import render, get_object_or_404

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        absolute_img_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, absolute_img_url)

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_entities = pokemon.entities.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        absolute_img_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, absolute_img_url)

    pokemon_info = {
        'title': pokemon.title,
        'title_ru': pokemon.title,
        'img_url': pokemon.image.url,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
    }

    pokemon_previous_evolution = pokemon.evolved_from
    if pokemon_previous_evolution:
        pokemon_info['previous_evolution'] = {
            "title_ru": pokemon_previous_evolution.title,
            "pokemon_id": pokemon_previous_evolution.id,
            "img_url": pokemon_previous_evolution.image.url,
        }

    pokemon_next_evolution = pokemon.next_evolutions.first()
    if pokemon_next_evolution:
        pokemon_info['next_evolution'] = {
            "title_ru": pokemon_next_evolution.title,
            "pokemon_id": pokemon_next_evolution.id,
            "img_url": pokemon_next_evolution.image.url,
        }

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_info})
