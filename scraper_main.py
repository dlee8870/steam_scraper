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
from scrape_app_ids import scrape_app_ids
from scrape_profile_ids import scrape_profile_ids


class Scraper:
    """A class representing the scraper settings.

    Instance Attributes
    - root_profile_id:
        The user's profile_id.
    - n:
        The number of games to scrape from this profile.
    - recurse_n:
        Determines how many games to scrape from other profiles.
    - depth:
        The depth of recursion; the smaller, the more similar the scraped games will be.

    Representation Invariants:
    - not(self.root_profile_id is None and self.root_games is None)
    """
    root_profile_id: str | int
    n: int
    recurse_n: int
    depth: int

    def __init__(self, root_profile_id: str | int, n: int, depth: int) -> None:
        if isinstance(root_profile_id, str):
            self.root_profile_id = convert_to_64bit(root_profile_id)
        else:
            self.root_profile_id = root_profile_id
        self.n = n
        self.depth = depth

    def scrape(self):
        root_games = scrape_app_ids(self.root_profile_id, self.n)  # set of app_ids
        return scrape_recursive(root_games)


def scrape_recursive(games: set[int]) -> set[int, dict]:
    ...  # Ahmed and Chris?


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


def convert_to_64bit(profile_id: str) -> int:
    url = f'https://steamid.net/?q={profile_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    converted = soup.find('input', {'id': 'results_steamid64'})
    return int(converted['value'])


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['requests', 'bs4', 'scrape_app_ids', 'scrape_profile_ids'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
