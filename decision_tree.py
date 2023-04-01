"""CSC111 Final Project: Steam Waiter

Module Description
===============================
This module contains code that creates a decision tree that outputs
personalized recommendations to a user.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Ahmed Hassini, Chris Oh, Andy Zhang, Daniel Lee
"""

from __future__ import annotations


class DecisionTree:
    """A preset decision tree (binary tree) used to adjust scores of games from the RecommendedGameNetwork

    Each game score will be adjusted based on where it ends up in the binary tree. The games in the rightmost node at
    the end will be increased the most, and the games in the left most node will have their score increased the least.

    Note that the order of questions DOES matter. The higher up the question the higher its importance.

    Preset Questions:
        1. Genre
        2. Price
        3. Release date
        4. Online component
        5. Multiplayer
        6. *Cross-platform* (Only ask this question if the user stated they prefer multiplayer games)

    Public Instance Attributes:
        - questions: The questions stated above
        - true_branch: If the answer is positive
        - false_branch: If the answer is negative
        -
    """


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
