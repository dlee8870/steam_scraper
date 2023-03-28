from __future__ import annotations

import steamscraper.steamscraper as scraper
from queue import Queue


class Game:
    """This object represents a video game and the relevant data associated with it

    Instance Attributes:
    - name: Name of the game
    - genre: Genre of the game
    - price: Price of the game
    - rating: Rating for this game
    - tributes: The number of games which have a directed edge pointing to itself
    - release_date: Realease date of the game
    - likeability: A score representing the probability of likeability of this game
    - recommended_games: Each key represents the recommended game and the associated value or the weight of the edge
        represents the percentage of reviewers that recommended the game
    """
    name: str
    genre: str
    price: float
    rating: float
    tributes: int
    likeability: float
    recomended_games: dict[Game, float]

    def __init__(self, name: str, genre: str, price: float, rating: float) -> None:
        self.name = name
        self.genre = genre
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
    # Public Instance Attributes
    #   - num_games: The number of games in the network
    #
    # Private Instance Attributes
    #   - _games: A collection of the games contained in this graph.
    #                    Keys: Game name, Values: Game object
    num_games: int
    _games: dict[str, Game]

    def __init__(self):
        self.num_games = 0
        self._games = {}

    def add_game_by_info(self, name: str, genre: str, price: float, rating: float) -> None:
        """Add a game  with the given name, score, and rating in the network.

        The new game is not adjacent to any other existing games.

        Preconditions:
        - name not in self._gameses
        """

        self._games[name] = Game(name, genre, price, rating)
        self.num_games += 1

    def add_game(self, game: Game) -> None:
        """Add a game to the network.

        The new game is not adjacent to any other existing games.

        Preconditions:
        - name not in self._gameses
        """

        self._games[game.name] = game
        self.num_games += 1

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
            self.add_game(init_game)
        if recommended_game not in self._games:
            self.add_game(recommended_game)

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
            if self._games[recommended_game] in self._games[init_game].recomended_games:
                self._games[init_game].recomended_games[recommended_game] = new_weight
            else:
                raise ValueError("init_game does not have an edge directed to recommended_game")
        else:
            raise ValueError("One of the games do not exist in this network.")

    def update_games_likeability(self) -> None:
        """Updates each games instance attribute likeability

        likeability is scored based on:
            - tributes
            -

        """


def create_game_recommendation_network(user_games: list[Game],
                                       num_recommendations: int = 10000) -> RecommnededGamesNetwork:
    """Takes in the user's top games from their profile
    then using the reviews on each game it will add recommended games to the network,
    returning a complete recommended game network
    """

    network = RecommnededGamesNetwork()

    #  Creating a new queue of the games to be added
    #  num_recommendations represents the maximum possible size of the queue (Optional)
    games_queue = Queue(num_recommendations)

    for game in user_games:
        games_queue.put_nowait(game)
        network.add_game(game)

    #  Keep looping till we added num_recommendations in the network
    #  Exit if the queue is empty (Occurs when not enough reviews on games were found)
    while not games_queue.empty() and network.num_games < num_recommendations:
        game = games_queue.get_nowait()

        # TODO: Andy's function in place for the empty list return a list of recommended games given game
        recommendations = []

        for recommended_game in recommendations:
            network.add_recommendation(game, recommended_game)  # TODO: figure out weight
            games_queue.put_nowait(recommended_game)

    return network
