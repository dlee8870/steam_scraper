"""CSC111 Final Project: Steam Waiter

Module Description
===============================
This module contains necessary code to scrape similar games based off a user's profile.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Andy Zhang, Daniel Lee, Ahmed Hassini, Chris Oh
"""

import requests
from scrape_app_ids import scrape_app_ids
from scrape_profile_ids import scrape_profile_ids


class Scraper:
    """A class representing the user initialized scraper settings.

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


def scrape_recursive(profile_id: int, n: int, d: int) -> list[int]:
    """Returns a list of the n most played games (in minutes) for the user corresponding to profile_id.
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


def convert_to_64bit(profile_id: str) -> int:
    url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
    params = {
        'key': '4957E3F30616447A483A7DBA9F26172E',
        'vanityurl': profile_id
    }
    response = requests.get(url, params).json()
    return int(response['response']['steamid'])


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['requests', 'scrape_app_ids', 'scrape_profile_ids'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
