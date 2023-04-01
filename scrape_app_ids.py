"""CSC111 Final Project: Steam Waiter

Module Description
===============================
This module contains necessary code to scrape relevant information about games
on the Steam platform.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Andy Zhang, Daniel Lee, Ahmed Hassini, Chris Oh
"""

import requests
from bs4 import BeautifulSoup


def get_json_response(profile_id: int) -> requests.models.Response.json:
    """Return the JSON response of the games list page of the user corresponding to profile_id.
    """
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
    response = requests.get(url + f'4957E3F30616447A483A7DBA9F26172E&steamid={str(profile_id)}&format=json')
    return response.json()


def scrape_app_ids(profile_id: int, n: int) -> set[int]:
    """Returns a set of the app ids of the n most played games (in minutes) for the user corresponding to profile_id.
    """
    games = get_json_response(profile_id)['response']['games']

    games_by_playtime = sorted(games, key=lambda g: g['playtime_forever'], reverse=True)

    return {games_by_playtime[i]['appid'] for i in range(n)}


def get_game_data(app_id: int) -> dict:
    """Scrape game data from the Steam store given an app id.

    Preconditions:
    - app_id corresponds to an existing game on the Steam platform.

    >>> get_game_data(400)
    {'name': 'Portal', 'genres': ['Puzzle', 'Puzzle Platformer', 'First-Person', '3D Platformer', 'Singleplayer',\
 'Sci-fi', 'Comedy', 'Female Protagonist', 'Funny', 'Physics', 'Action', 'Story Rich', 'Classic', 'Platformer',\
 'Science', 'Atmospheric', 'FPS', 'Dark Humor', 'Short', 'Adventure'], 'is_multiplayer': False,\
 'has_online_component': False, 'price': 'CDN$ 12.99', 'rating': ''}
    """
    url = f"https://store.steampowered.com/app/{app_id}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Get game name
    name = soup.select_one("div.apphub_AppName").text.strip()

    # Get game description
    description = soup.find('div', {'class': 'game_description_snippet'}).text.strip()

    # Get game genres
    genres = [genre.text.strip() for genre in soup.select("a.app_tag")]

    # Get game player modes (not foolproof)
    is_multiplayer = 'multiplayer' in description.lower() or 'multi-player' in description.lower()

    # Get game online component (not foolproof)
    has_online_component = 'online' in description.lower()

    # Get game price
    price_section = soup.select_one("div.game_purchase_price")
    price = ""
    if price_section:
        price = price_section.text.strip()

    # Get game rating (This doesn't work yet)
    # rating_section = soup.select_one("div.user_reviews_summary_row span.game_review_summary")
    rating = ""
    # if rating_section:
    #     rating_text = rating_section["data-tooltip-text"]
    #     rating = float(rating_text.replace('%', '').replace(',', ''))
    #     rating = rating / 100

    return {
        "name": name,
        "genres": genres,
        "is_multiplayer": is_multiplayer,
        "has_online_component": has_online_component,
        "price": price,
        "rating": rating
    }


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['requests', 'bs4'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
