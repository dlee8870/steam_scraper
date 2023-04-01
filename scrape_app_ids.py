"""CSC111 Final Project: Steam Waiter

Module Description
===============================
This module contains necessary code to scrape the app ids given a user's profile id.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Andy Zhang, Daniel Lee, Ahmed Hassini, Chris Oh
"""

import requests


def get_json_response(params: dict) -> requests.models.Response.json:
    """Return the JSON response of the games list page given params.

    Preconditions:
        - len(profile_id) == 17
        - the profile is public
    """
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    response = requests.get(url=url, params=params)
    return response.json()['response']


def scrape_app_ids(profile_id: int, n: int) -> list[int]:
    """Returns a list of the app ids of the n most played games (in minutes) for the user corresponding to profile_id.
    Return an empty list if they have hidden game details. If they have less than n games, return all the games.

    Preconditions:
        - len(profile_id) == 17
        - n > 0
    """
    params = {
        'key': '4957E3F30616447A483A7DBA9F26172E',
        'steamid': str(profile_id),
        'format': 'json'
    }
    json_response = get_json_response(params)

    if not json_response:
        return []

    games = json_response['games']
    games_by_playtime = sorted(games, key=lambda g: g['playtime_forever'], reverse=True)

    if len(games_by_playtime) < n:
        return [game['appid'] for game in games_by_playtime]
    else:
        return [games_by_playtime[i]['appid'] for i in range(n)]


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
