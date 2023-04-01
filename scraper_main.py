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
from typing import Optional


class Scraper:
    """A class representing the scraper settings.
    Instance Attributes
    - address:
        The address (i.e., unique identifier) of this node.
        This replaces the "item" attribute in the _Vertex class from lecture.
    - channels:
        A mapping containing the channels for this node.
        Each key in the mapping is the address of a neighbour node,
        and the corresponding value is the channel leading to that node.
        This replaces the "neighbours" attribute in the _Vertex class from lecture.

    Representation Invariants:
    - self.address not in self.channels
    - all(self in self.channels[addy].endpoints for addy in self.channels)
    """
    root_profile_id: Optional[str | int]
    root_games: Optional[set[int]]  # set of game app_ids
    n: int  # Determines how many games to scrape from this user.
    recurse_n: int  # Determines how many games to scrape from other users
    d: int  # Depth of recursion, the smaller, the more "similar"

    def __init__(self, root_profile_id: str | int, n: int, d: int) -> None:
        # Andy do you mean root_profile_id here
        if isinstance(root_profile_id, str):
            self.root_profile_id = convert_to_64bit(root_profile_id)
        else:
            self.root_profile_id = root_profile_id
        self.n = n
        self.d = d

    def scrape(self):
        starting_games = scrape_games(self.root_profile_id, self.n)
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
