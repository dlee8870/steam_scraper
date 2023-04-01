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


def get_json_response(profile_id: int) -> requests.models.Response.json:
    """Return the JSON response of the games list page of the user corresponding to profile_id.
    """
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
    response = requests.get(url + f'4957E3F30616447A483A7DBA9F26172E&steamid={str(profile_id)}&format=json')
    return response.json()


def scrape_games(profile_id: int, n: int) -> list[dict]:
    """Returns a list of the n most played games (in minutes) for the user corresponding to profile_id.
    """
    games = get_json_response(profile_id)['response']['games']

    games_by_playtime = sorted(games, key=lambda g: g['playtime_forever'], reverse=True)

    return games_by_playtime[0:n]


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
