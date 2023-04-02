"""CSC111 Final Project: Steam Waiter

Module Description
===============================
This module contains necessary code to scrape relevant information about games
on the Steam platform.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Andy Zhang, Daniel Lee, Ahmed Hassini, Chris Oh
"""

from bs4 import BeautifulSoup
import requests
from games_network import Game


def get_game_data(app_id: int) -> Game:
    """Scrape game data from the Steam store given an app id.

    Preconditions:
    - app_id corresponds to an existing game on the Steam platform.

    >>> game1 = get_game_data(1677740)
    >>> game1.name
    'Stumble Guys'
    >>> game1.rating
    0.9

    >>> game2 = get_game_data(1023940)
    >>> game2.genres
    {'Education', 'Software Training', 'VR'}
    >>> game2.multiplayer
    False
    >>> game2.price
    135.99
    """
    url = f"https://store.steampowered.com/app/{app_id}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Get game name
    name = soup.select_one("div.apphub_AppName").text.strip()

    # Get game description
    description = soup.find('div', {'class': 'game_description_snippet'}).text.strip()

    # Get game genres
    genres = {genre.text.strip() for genre in soup.select("a.app_tag")}

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
        # Strip any dollar signs and currency symbols
        price = ''.join(filter(str.isdigit, price))
        if price:
            price = float(price) / 100
        else:
            price = 0
    # If there is no price section, the game is free
    else:
        price = 0

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

    return Game(name, genres, price, has_online_component, is_multiplayer, rating, int(release_year))


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['bs4', 'requests'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'disable': ['too-many-branches', 'too-many-locals'],
        'max-line-length': 120
    })
