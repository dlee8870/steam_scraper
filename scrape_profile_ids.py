"""CSC111 Final Project: Steam Waiter

Module Description
===============================
This module contains necessary code to scrape profile ids from reviews for a given game.
Main documentation utilized: https://partner.steamgames.com/doc/store/getreviews

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Andy Zhang, Daniel Lee, Ahmed Hassini, Chris Oh
"""

import requests


# def scrape_profile_ids(app_id: int, n: int) -> list[int]:
#     """Return a list of the users corresponding to the top n most helpful reviews of the game.
#
#     Preconditions:
#         - n >= 0
#
#     >>> scrape_profile_ids(730, 2)
#     ['76561198110513339', '76561198388416030']
#     """
#     params = {
#         'json': 1,
#         'filter': 'all',
#         'language': 'english',
#         'day_range': 101010101010101010101010101010,
#         'cursor': '*'.encode(),
#         'review_type': 'positive',
#         'purchase_type': 'all',
#         'num_per_page': 100
#     }
#
#     reviews = []
#
#     while n > 0:
#         params['num_per_page'] = min(n, 100)  # each response cursor yields at most 100 reviews
#         n -= 100
#         response = get_json_response(app_id, params)
#         if "cursor" not in response:
#             return []
#         params['cursor'] = response['cursor'].encode()
#         reviews += response['reviews']
#
#     return [int(review['author']['steamid']) for review in reviews]
#

def get_reviews(appid, params={'json': 1}):
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url + str(appid), params=params, headers={'User-Agent': 'Mozilla/5.0'})
    return response.json()


def scrape_profile_ids(app_id, n):
    reviews = []
    cursor = '*'
    params = {
        'json': 1,
        'filter': 'all',
        'language': 'english',
        'day_range': 9223372036854775807,
        'review_type': 'all',
        'purchase_type': 'all'
    }

    while n > 0:
        params['cursor'] = cursor.encode()
        params['num_per_page'] = min(100, n)
        n -= 100

        response = get_reviews(app_id, params)
        cursor = response['cursor']
        reviews += response['reviews']

        if len(response['reviews']) < 100: break

    return [int(review['author']['steamid']) for review in reviews]


def get_json_response(app_id: int, params: dict) -> requests.models.Response.json:
    """Return the JSON response of the game reviews page
    Note: API skips age checks and violence warnings.

    Preconditions:
        - app_id corresponds to a game on Steam
    """
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url + str(app_id), params)

    return response.json()


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['requests'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
