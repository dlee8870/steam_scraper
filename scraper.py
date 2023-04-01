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
        The starting profile_id (64 bit). Games recommended will be similar to the games in this profile.
    - n:
        The number of games to scrape from this profile.
    - recurse_n:
        Determines how many games to scrape from other profiles.
    - d:
        The depth of recursion; the smaller, the more similar the scraped games will be.

    Representation Invariants:
    - not(self.root_profile_id is None and self.root_games is None)
    - root_profile_id must be public and more specifically, the games list must be accessible
    """
    root_profile_id: str | int
    n: int
    recurse_n: int
    d: int

    def __init__(self, root_profile_id: str | int, n: int, d: int) -> None:
        """...
        """
        if isinstance(root_profile_id, str):
            self.root_profile_id = convert_to_64bit(root_profile_id)
        else:
            self.root_profile_id = root_profile_id
        self.n = n
        self.d = d

    def scrape(self):
        """...
        """
        return scrape_recursive(self.root_profile_id, self.n, self.d)


def scrape_recursive(profile_id: int, n: int, d: int) -> set[int]:
    """...
    """
    if d == 0:
        return scrape_app_ids(profile_id, n)
    else:
        app_ids = scrape_app_ids(profile_id, n)

        for app_id in app_ids:
            profile_ids = scrape_profile_ids(app_id, n)
            for profile_id in profile_ids:
                app_ids = app_ids.union(scrape_recursive(profile_id, n, d - 1))

        return app_ids


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


def convert_to_64bit(profile_id: str) -> int:
    url = f'https://steamid.net/?q={profile_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    converted = soup.find('input', {'id': 'results_steamid64'})
    return int(converted['value'])

# if __name__ == '__main__':
#     import python_ta
#     import python_ta.contracts
#
#     import doctest
#
#     doctest.testmod()
#
#     python_ta.check_all(config={
#         'extra-imports': ['requests', 'bs4', 'scrape_app_ids', 'scrape_profile_ids'],
#         # the names (strs) of imported modules
#         'allowed-io': [],  # the names (strs) of functions that call print/open/input
#         'max-line-length': 120
#     })
