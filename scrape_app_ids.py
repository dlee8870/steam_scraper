"""CSC111 Final Project: Steam Waiter

Module Description
===============================
This module contains necessary code to scrape the app ids given a user's profile id.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Andy Zhang, Daniel Lee, Ahmed Hassini, Chris Oh
"""

import requests
from bs4 import BeautifulSoup


def get_json_response(profile_id: int) -> requests.models.Response.json:
    """Return the JSON response of the games list page of the user corresponding to profile_id.

    Preconditions:
        - len(profile_id) == 17
        - the profile is public
    """
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
    response = requests.get(url + f'4957E3F30616447A483A7DBA9F26172E&steamid={str(profile_id)}&format=json')
    return response.json()['response']


def scrape_app_ids(profile_id: int, n: int) -> set[int]:
    """Returns a set of the app ids of the n most played games (in minutes) for the user corresponding to profile_id.
    Return an empty set if they have hidden game details.

    Preconditions:
        - len(profile_id) == 17
        - n > 0
    """
    json_response = get_json_response(profile_id)
    if not json_response:
        return set()

    games = json_response['games']

    games_by_playtime = sorted(games, key=lambda g: g['playtime_forever'], reverse=True)

    return {games_by_playtime[i]['appid'] for i in range(n)}


def get_game_data(app_id: int) -> dict:
    """Scrape game data from the Steam store given an app id.

    Preconditions:
    - app_id corresponds to an existing game on the Steam platform.

    >>> get_game_data(1677740)
    {'name': 'Stumble Guys', 'genres': ['Free to Play', 'Multiplayer', 'Action', 'Casual', '3D', '3D Platformer', \
'Colorful', 'Family Friendly', 'Battle Royale', 'Cute', 'Cartoony', 'Racing', 'Character Customization', \
'Massively Multiplayer', 'PvP', 'Nudity', 'Physics', 'Comedy', 'Funny', 'Indie'], 'is_multiplayer': True, \
'has_online_component': True, 'price': 'Free', 'rating': 0.9, 'release_date': '2021'}
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

    # Get game player modes
    is_multiplayer = 'multiplayer' in description.lower() or 'multi-player' in description.lower() or \
                     any('multiplayer' in tag.text.lower() for tag in soup.select('a.app_tag')) or \
                     any('multi-player' in tag.text.lower() for tag in soup.select('a.app_tag'))

    # Get game online component
    has_online_component = 'online' in description.lower() or 'online' in genres or \
                           any('online' in tag.text.lower() for tag in soup.select('a.app_tag'))

    # Get game price
    price_section = soup.select_one("div.game_purchase_price")
    if price_section:
        price = price_section.text.strip()
    # If there is no price section, the game is free
    else:
        price = "Free"

    # Get game rating
    review_summary = soup.select_one("div.user_reviews_summary_row")
    rating = 0.0
    if review_summary:
        overall_review = review_summary.select_one("span.game_review_summary").text.strip().replace(",", "")
        if overall_review == 'Overwhelmingly Positive':
            rating = 1.0
        elif overall_review == 'Very Positive':
            rating = 0.90
        elif overall_review == 'Positive':
            rating = 0.80
        elif overall_review == 'Mostly Positive':
            rating = 0.7
        elif overall_review == 'Mixed':
            rating = 0.5
        elif overall_review == 'Mostly Negative':
            rating = 0.4
        elif overall_review == 'Negative':
            rating = 0.3
        elif overall_review == 'Very Negative':
            rating = 0.2
        else:
            rating = 0.1

    # Get game release year
    release_date_section = soup.select_one("div.date")
    if release_date_section:
        release_year = release_date_section.text.strip()[-4:]
    else:
        release_year = ""

    return {
        "name": name,
        "genres": genres,
        "is_multiplayer": is_multiplayer,
        "has_online_component": has_online_component,
        "price": price,
        "rating": rating,
        "release_date": release_year
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
