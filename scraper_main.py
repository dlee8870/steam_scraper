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
from scrape_games import scrape_games


class Scraper:
    """A class representing the scraper settings.
    ...
    """
    root_profile_id: str | int
    root_games: list[dict]
    n: int  # Determines how many games to scrape from this user.
    recurse_n: int  # Determines how many games to scrape from other users
    d: int  # Depth of recursion, the smaller, the more "similar"

    def __init__(self, profile_id: str | int, n: int, d: int) -> None:
        # Andy do you mean root_profile_id here
        if isinstance(profile_id, str):
            self.profile_id = convert_to_64bit(profile_id)
        else:
            self.profile_id = profile_id
        self.n = n
        self.d = d

    def scrape(self):
        starting_games = scrape_games(self.profile_id, self.n)
        scrape_recursive(starting_games)


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
