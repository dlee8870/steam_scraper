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
        root_games = scrape_app_ids(self.root_profile_id, self.n)
        scrape_recursive(root_games)


def scrape_recursive(games: list[dict]):
    scrape_games()
    for game in games:
        ...


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
        'extra-imports': ['requests', 'bs4', 'scrape_games'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
