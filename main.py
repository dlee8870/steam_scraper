from __future__ import annotations
import steamscraper.steamscraper as scraper
from typing import Any


class Vertex:
    """A vertex in a graph.

    Instance Attributes:
    - game_name: Name of the game
    - game_price: Price of the game
    - game_rating: Rating for this game
    - game_score: Overall score for this game
    """
    game_name: str
    game_price: float
    game_rating: float
    game_score: float
    neighbours: dict[Vertex, float]

    def __init__(self, game_name: str, game_price: float, game_rating: float, neighbours: dict[Vertex, float]) -> None:
        self.game_name = game_name
        self.game_price = game_price
        self.game_rating = game_rating
        self.game_score = self.calculate_score()
        self.neighbours = neighbours

    def calculate_score(self) -> float:
        """Calculate the score of the game based on its price, rating, etc."""
        # Come up with a cool algorithm here.
        return self.game_rating


class DirectedGraph:
    """A directed graph.
    """
    # Private Instance Attributes
    #       - _vertices: A collection of the games contained in this graph.
    #                    Maps a game to another Vertex instance.
    _vertices: dict[Any, Vertex]

    def __init__(self):
        self._vertices = {}

    def add_vertex(self, game_name: str, game_price: float, game_rating: float) -> None:
        """Add a game vertex with the given game_name and game_score in the directed graph.

        The new vertex is not adjacent to any other existing vertices.

        Preconditions:
        - game_name not in self._vertices
        """
        self._vertices[game_name] = Vertex(game_name, game_price, game_rating, {})

    def add_edge(self, start_vertex: str, end_vertex: str, weight: float = 0.0) -> None:
        """Add an edge from the start_vertex to the end_vertex with the given vertices in this graph.
        Assign a default edge weight of 0.

        The edge represents a one-way recommendation, where the start_vertex game recommends the end_vertex
        game. The weight value represents the strength of a recommendation from a game to another game. The
        higher the weight, the stronger the recommendation.
        """
        if start_vertex in self._vertices and end_vertex in self._vertices:
            self._vertices[start_vertex].neighbours[self._vertices[end_vertex]] = weight
        else:
            raise ValueError

    def get_neighbours(self, game_name: str) -> dict:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if game_name in self._vertices:
            return self._vertices[game_name].neighbours
        else:
            raise ValueError

    def update_edge_weight(self, game1_name: str, game2_name: str, new_weight: float) -> None:
        """Update the weight of the edge between game1 and game2 to new_weight."""
        if game1_name in self._vertices and game2_name in self._vertices:
            game1 = self._vertices[game1_name]
            game2 = self._vertices[game2_name]
            if game2 in game1.neighbours:
                game1.neighbours[game2] = new_weight
        else:
            raise ValueError


if __name__ == '__main__':
    ...
