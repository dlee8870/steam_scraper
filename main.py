from __future__ import annotations
import steamscraper.steamscraper as scraper
from typing import Any


class Game:
    """This object represents a video game and the relevant data associated with it

    Instance Attributes:
    - name: Name of the game
    - price: Price of the game
    - rating: Rating for this game
    - tributes: The number of games which have a directed edge pointing to itself
    - release_date: Realease date of the game
    - likeability: A score representing the probability of likeability of this game
    - recommended_games: Each key represents the recommended game and the associated value or the weight of the edge
        represents the percentage of reviewers that recommended the game
    """
    name: str
    price: float
    rating: float
    tributes: int
    likeability: float
    recomended_games: dict[Game, float]

    def __init__(self, name: str, price: float, rating: float) -> None:
        self.name = name
        self.price = price
        self.rating = rating
        self.tributes = 0
        self.game_score = self.calculate_score()
        self.recomended_games = {}

    def calculate_score(self) -> float:
        """Calculate the score of the game based on its price, rating, etc."""
        # Come up with a cool algorithm here.
        return self.rating


class RecommnededGamesNetwork:
    """A directed graph where each vertex represents a game object and each directed edge represents a
        recommendation.
    """
    # Private Instance Attributes
    #   - _games: A collection of the games contained in this graph.
    #                    Keys: Game name, Values: Game object
    _games: dict[str, Game]

    def __init__(self):
        self._games = {}

    def add_game(self, name: str, price: float, rating: float) -> None:
        """Add a game  with the given name, score, and rating in the network.

        The new game is not adjacent to any other existing games.

        Preconditions:
        - name not in self._gameses
        """

        self._games[name] = Game(name, price, rating)

    def add_recommendation(self, init_game: Game, recommended_game: Game, weight: float = 0.0) -> None:
        """Add an edge from the init_game to the recommended_game with the given game names in this graph.
        Assign a default edge weight of 0.

        The edge represents a one-way recommendation, where the init_game recommends the recommended_game.
        The weight value represents the strength of a recommendation from a game to another game.

        Note that the tribute attribute of recommended_game gets updates

        If any of the games are not in the network then add them to the network
        """

        #  Adding games to the network if they are not already in it
        if init_game.name not in self._games:
            self._games[init_game.name] = init_game
        if recommended_game not in self._games:
            self._games[recommended_game] = recommended_game

        #  Adding a one way edge
        init_game.recomended_games[recommended_game] = weight

        #  Updating tributes attribute for recommended game
        recommended_game.tributes += 1

    def get_recommendations(self, game: str) -> set[Game]:
        """Return the set of games recommended by game.

        Note that the objects are returned, not the game names

        Raise a ValueError if the game is not in the network.
        """

        if game not in self._games:
            raise ValueError("Game name not found in network.")
        else:
            return set(self._games[game].recomended_games.keys())

    def update_edge_weight(self, init_game: str, recommended_game: str, new_weight: float) -> None:
        """Update the weight of the edge between init_game and recommended_game to new_weight.


        If either game is not in the network then raise a ValueError
        If init_game does not recommend recommended_game raise a ValueError

        """

        if init_game in self._games and recommended_game in self._games:
            if self._games[recommended_game] in self._games[init_game].recomended_games:
                self._games[init_game].recomended_games[recommended_game] = new_weight
            else:
                raise ValueError("init_game does not have an edge directed to recommended_game")
        else:
            raise ValueError("One of the games do not exist in this network.")


if __name__ == '__main__':
    ...
