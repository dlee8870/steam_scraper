"""CSC111 Final Project: Steam Waiter

Module Description
===============================
A module that contains classes for representing a game, a directed graph
of recommended games, and functions for updating and retrieving recommendations.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Ahmed Hassini, Chris Oh, Andy Zhang, Daniel Lee
"""

from __future__ import annotations
from queue import Queue
from typing import Optional
from bs4 import BeautifulSoup
import requests
from scrape_profile_ids import scrape_profile_ids
from scrape_app_ids import scrape_app_ids


class Game:
    """This object represents a video game and the relevant data associated with it.

    Instance Attributes:
    - name: Name of the game
    - genres: Genres of the game
    - price: Price of the game
    - online: Whether there is an online component to the game
    - multiplayer: Whether there is a multiplayer option
    - rating: Rating for this game
    - tributes: A list of games that have a directed edge pointing to this game
    - release_date: Release year of the game
    - likeability: A score representing the likeability of this game
    - recommended_games: Each key represents a recommended game from this game and an associated value.
                            This value, also known as the weight of the connection/edge, represents the percentage
                            of reviewers who play this game that recommended the other game.

    Representation Invariants:
    - self.name != ''
    - self.price >= 0
    - self.rating >= 0
    - self.release_date >= 0
    - self.likeability >= 0
    """
    name: str
    genres: set[str]
    price: float
    online: bool
    multiplayer: bool
    rating: float
    tributes: list[Game]
    release_date: int
    likeability: float
    recommended_games: dict[Game, float]

    def __init__(self, name: str, genres: set[str], price: float, online: bool,
                 multiplayer: bool, rating: float, release_date: int) -> None:
        # PythonTA says max number of parameters is 5. Maybe ignore this one.
        self.name = name
        self.genres = genres
        self.price = price
        self.online = online
        self.multiplayer = multiplayer
        self.rating = rating
        self.release_date = release_date
        self.tributes = []
        self.likeability = 0
        self.recommended_games = {}

    def update_game_likeability(self, max_tributes: int) -> None:
        """Updates game instance attribute likeability.

        Preconditions:
        - max_tributes >= 0

        likeability is scored based on:
            - tributes
            - ratings
            - tributes weight
        """
        tribute_score = len(self.tributes) / max_tributes

        accumulated_weight = 0

        for tribute in self.tributes:
            accumulated_weight += tribute.recommended_games[self]

        tributes_weight = accumulated_weight / len(self.tributes)

        self.likeability = tributes_weight + tribute_score + self.rating


class RecommendedGamesNetwork:
    """A directed graph where each vertex represents a game object and each directed edge represents a
        recommendation.

    Representation Invariants:
    - self.num_games >= 0
    - self.max_tributes >= 0
    """
    # Public Instance Attributes
    #   - num_games: The number of games in the network.
    #   - max_tributes: The max number of tributes in the network.
    #
    # Private Instance Attributes
    #   - _games: A collection of the games contained in this graph.
    #                    Keys: Game name, Values: Game object
    num_games: int
    _games: dict[str, Game]
    max_tributes: int

    def __init__(self) -> None:
        self.num_games = 0
        self._games = {}
        self.max_tributes = 0

    def add_game_by_info(self, name: str, genre: set[str], price: float, rating: float, online: bool,
                         multiplayer: bool, release_date: int) -> None:
        """Add a game with the given name, score, and rating in the network.

        The new game is not adjacent to any other existing games.

        Preconditions:
        - name not in self._games
        """
        self._games[name] = Game(name, genre, price, online, multiplayer, rating, release_date)
        self.num_games += 1

    def add_game(self, game: Game) -> None:
        """Add a game to the network.

        The new game is not adjacent to any other existing games.

        Preconditions:
        - name not in self._games
        """
        self._games[game.name] = game
        self.num_games += 1

    def add_recommendation(self, init_game: Game, recommended_game: Game, weight: float = 0.0) -> None:
        """Add an edge from the init_game to the recommended_game with the given game names in this graph.
        Assign a default edge weight of 0.

        The edge represents a one-way recommendation, where the init_game recommends the recommended_game.
        The weight value represents the strength of a recommendation from init_game to recommended_game.

        Note that the tribute attribute of recommended_game gets updates.

        If any of the games are not in the network, then add them to the network.
        """
        #  Adding games to the network if they are not already in it
        if init_game.name not in self._games:
            self.add_game(init_game)
        if recommended_game not in self._games:
            self.add_game(recommended_game)

        #  Adding a one way edge
        init_game.recommended_games[recommended_game] = weight

        #  Updating tributes
        recommended_game.tributes.append(init_game)

        #  Updating tributes attribute for recommended game
        self.max_tributes = max(self.max_tributes, len(recommended_game.tributes))

    def get_recommendations(self, game: str) -> set[Game]:
        """Return the set of games recommended by game.

        Note that the objects are returned, not the game names.

        Raise a ValueError if the game is not in the network.
        """
        if game not in self._games:
            raise ValueError("Game name not found in network.")
        else:
            return set(self._games[game].recommended_games.keys())

    def get_games_to_likeability(self) -> dict[Game, float]:
        """Returns a dictionary where the keys are the games in the network
        and the values are the likeability scores
        """
        return {game: game.likeability for game in self._games.values()}

    def get_games(self) -> set[Game]:
        """Returns a set of the games in the network."""

        return set(self._games.values())

    def update_edge_weight(self, init_game: str, recommended_game: str, new_weight: float) -> None:
        """Update the weight of the edge between init_game and recommended_game to new_weight.

        If either game is not in the network then raise a ValueError
        If init_game does not recommend recommended_game raise a ValueError
        """
        if init_game in self._games and recommended_game in self._games:
            if self._games[recommended_game] in self._games[init_game].recommended_games:
                updated_game = self._games[recommended_game]
                self._games[init_game].recommended_games[updated_game] = new_weight
            else:
                raise ValueError("init_game does not have an edge directed to recommended_game")
        else:
            raise ValueError("One of the games do not exist in this network.")

    def update_games_likeability(self) -> None:
        """Updates each games instance attribute likeability.

        Likeability score will be between 0 and 3, inclusive, where 3 indicates the highest likeability for a game.

        Likeability is scored based on:
            - tributes
            - ratings
            - tributes weight
        """
        for game in self._games.values():
            game.update_game_likeability(self.max_tributes)


def create_recommendation_network(user_app_ids_to_games: dict[int, Game],
                                  num_recommendations: int = 111) -> RecommendedGamesNetwork:
    """Takes in the user's top games from their profile
    then using the reviews on each game it will add recommended games to the network,
    returning a complete recommended game network
    """
    network = RecommendedGamesNetwork()

    visited_profile_ids = set()
    q = Queue()  # Queue of app ids
    app_id_to_game = user_app_ids_to_games.copy()

    for app_id in user_app_ids_to_games:
        q.put_nowait(app_id)  # Adding starting games to queue
        network.add_game(user_app_ids_to_games[app_id])  # Adding starting games to network

    #  Keep looping till we added num_recommendations in the network
    #  Exit if the queue is empty (Occurs when not enough reviews on games were found)
    app_ids_to_appearances = {}
    while not q.empty() and network.num_games < num_recommendations:
        curr_app_id = q.get_nowait()
        profile_ids = scrape_profile_ids(curr_app_id, 5)
        print(f"Completeness: {round((network.num_games / num_recommendations) * 100, 1)}")

        for profile_id in profile_ids:
            if profile_id not in visited_profile_ids and network.num_games < num_recommendations:
                app_ids = scrape_app_ids(profile_id, 5)
                visited_profile_ids.add(profile_id)
                for app_id in app_ids:
                    if app_id not in app_ids_to_appearances:
                        q.put_nowait(app_id)
                        get_game = get_game_data(app_id)
                        if get_game is None:
                            continue
                        app_id_to_game[app_id] = get_game_data(app_id)
                        app_ids_to_appearances[app_id] = 1
                    else:
                        app_ids_to_appearances[app_id] += 1

                    total_game_appearances = sum([app_ids_to_appearances[key] for key in app_ids_to_appearances])
                    network.add_recommendation(app_id_to_game[curr_app_id],
                                               app_id_to_game[app_id],
                                               app_ids_to_appearances[app_id] / total_game_appearances)

    network.update_games_likeability()

    return network


def get_game_data(app_id: int) -> Optional[Game]:
    """Scrape game data from the Steam store given an app id.

    Preconditions:
    - app_id corresponds to an existing game on the Steam platform.

    >>> game1 = get_game_data(1677740)
    >>> game1.name
    'Stumble Guys'
    >>> game1.rating
    0.9

    >>> game2 = get_game_data(1023940)
    >>> game2.multiplayer
    False
    >>> game2.price
    135.99
    """
    url = f"https://store.steampowered.com/app/{app_id}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Get game name
    try:
        name = soup.select_one("div.apphub_AppName").text.strip()
    except AttributeError:
        return None

    # Get game description
    description = soup.select_one('div', {'class': 'game_description_snippet'}).text.strip()

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
        'extra-imports': ['queue', 'bs4', 'requests', 'scrape_profile_ids', 'scrape_app_ids'],
        'allowed-io': [],
        'disable': ['too-many-instance-attributes', 'too-many-arguments', 'too-many-locals', 'too-many-branches'],
        'max-line-length': 120
    })
