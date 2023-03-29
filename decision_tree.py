from __future__ import annotations

class DecisionTree:
    """A preset decision tree (binary tree) used to adjust scores of games from the RecommendedGameNetwork

    Each game score will be adjusted based on where it ends up in the binary tree. The games in the rightmost node at
    the end will be increased the most, and the games in the left most node will have their score increased the least.

    Note that the order of questions DOES matter. The higher up the question the higher it's importance.

    Preset Questions:
        1. Genre
        2. Price
        3. Release date
        4. Online component
        5. Multiplayer
        6. *Cross-paltform* (Only ask this question if the user stated they prefer multiplayer games)

    Public Instance Attributes:
        - questions: The questions stated above
        - true_branch: If the answer is positive
        - false_branch: If the answer is negative
        -

    """
