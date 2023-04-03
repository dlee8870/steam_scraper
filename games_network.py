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
from scrape_profile_ids import scrape_profile_ids
from scrape_app_ids import scrape_app_ids
from scrape_game_data import get_game_data


class Game:
    """This object represents a video game and the relevant data associated with it.

    Instance Attributes:
    - name: Name of the game
    - genres: Genre of the game
    - price: Price of the game
    - online: Whether there is an online component to the game
    - multiplayer: Whether there is a multiplayer option
    - rating: Rating for this game
    - tributes: A list of games that have a directed edge pointing to this game
    - release_date: Release date of the game
    - likeability: A score representing the likeability of this game
    - recommended_games: Each key represents a recommended game from this game and an associated value.
                            This value, also known as the weight of the connection/edge, represents the percentage
                            of reviewers who play this game that recommended the other game.
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
    # PythonTA says max number of attributes is 8

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


def create_recommendation_network(user_games: dict[Game, int],
                                  num_recommendations: int = 10000) -> RecommendedGamesNetwork:
    """Takes in the user's top games from their profile
    then using the reviews on each game it will add recommended games to the network,
    returning a complete recommended game network
    """
    network = RecommendedGamesNetwork()

    #  Creating a new queue of the games to be added
    #  num_recommendations represents the maximum possible size of the queue (Optional)
    games_queue = Queue(num_recommendations)
    visited_games = set()

    for game in user_games:
        games_queue.put_nowait(game)
        network.add_game(game)

    #  Keep looping till we added num_recommendations in the network
    #  Exit if the queue is empty (Occurs when not enough reviews on games were found)
    while not games_queue.empty() and network.num_games < num_recommendations:
        game = games_queue.get_nowait()
        visited_games.add(game)
        app_id = user_games[game]

        recommendations = recommendation_network_helper(app_id)
        total_weight = sum(recommendations[app_id] for app_id in recommendations)

        for recommended_app_id in recommendations:
            recommended_game = get_game_data(recommended_app_id)
            game_weight = recommendations[recommended_app_id] / total_weight
            network.add_recommendation(game, recommended_game, game_weight)
            if recommended_game not in visited_games:
                games_queue.put_nowait(recommended_game)

    return network


def recommendation_network_helper(app_id: int) -> dict:
    """Obtains a list of recommendations whose keys are the recommended game and the
    values are the number of times it appears in a user's review.

    Preconditions:
    - app_id is a valid game ID on Steam
    """
    user_ids = scrape_profile_ids(app_id, 5)

    recommendations = {}

    for user_id in user_ids:
        game_app_ids = scrape_app_ids(user_id, 5)

        for game_app_id in game_app_ids:
            if game_app_id in recommendations:
                recommendations[game_app_id] += 1
            else:
                recommendations[game_app_id] = 1

    return recommendations


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    import doctest
    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['queue', 'math'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
