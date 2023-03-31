from __future__ import annotations
import steamscraper.steamscraper as scraper
from queue import Queue
import math


class Game:
    """This object represents a video game and the relevant data associated with it

    Instance Attributes:
    - name: Name of the game
    - genre: Genre of the game
    - price: Price of the game
    - online: Whether there is an online component to the agme
    - multiplayer: Whether there is a multiplayer option
    - rating: Rating for this game
    - tributes: The number of games which have a directed edge pointing to itself
    - release_date: Release date of the game
    - likeability: A score representing the probability of likeability of this game
    - recommended_games: Each key represents a recommended game from this game and an associated value.
                            This value, also known as the weight of the connection/edge, represents the percentage
                            of reviewers who play this game that recommended the other game.
    """
    name: str
    genre: str
    price: float
    online: bool
    multiplayer: bool
    rating: float
    tributes: list[Game]
    release_date: int
    likeability: float
    recommended_games: dict[Game, float]

    def __init__(self, name: str, genre: str, price: float, online: bool,
                 multiplayer: bool, rating: float, release_date: int) -> None:
        self.name = name
        self.genre = genre
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
    max_tributes = int

    def __init__(self):
        self.num_games = 0
        self._games = {}
        self.max_tributes = 0

    def add_game_by_info(self, name: str, genre: str, price: float, rating: float, online: bool,
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

        Note that the tribute attribute of recommended_game gets updates

        If any of the games are not in the network then add them to the network
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
        #  recommended_game.tributes += 1
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


def create_game_recommendation_network(user_games: list[Game],
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

        # TODO: Andy's function in place for the empty list return a list of recommended games given game
        # TODO: Andy get weight, calculated based on how many reviews recommended the game
        recommendations = []

        for recommended_game in recommendations:
            network.add_recommendation(game, recommended_game)  # TODO: figure out weight
            if recommended_game not in visited_games:
                games_queue.put_nowait(recommended_game)

    return network


#  TODO: This function will be used in the decision tree when we get the user's preference
def price_similarity(init_game_price: float, recommended_game_price: float) -> float:
    """Return a similarity score between 0 and 1, inclusive, given the price of a game
    and a recommended game.

    >>> price_similarity(5, 10)
        0.9900498337491681
    >>> price_similarity(500, 1000)
        0.36787944117144233
    >>> price_similarity(10, 5000000000)
        0.0
    """
    k = 0.002  # tuning parameter
    x = abs(init_game_price - recommended_game_price)
    return math.exp(-k * x)
