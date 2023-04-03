"""CSC111 Final Project: Steam Waiter
Module Description
===============================
This module contains necessary code to run our entire program.
Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Chris Oh, Ahmed Hassini, Andy Zhang, Daniel Lee
"""
from scrape_app_ids import scrape_app_ids
from games_network import create_recommendation_network
from input_data import run_tkinter

# Note to self: Need to split up program into the following files according to assignment page:
#   - Reading data (done)
#   - Computing on data
#   - Display of data
#   - main.py (has a main block to run entire program from start to finish.)\

def profile_id_to_top_games(user_id: int | str) -> list[int]:
    """Given the user's profile id return a list of their top game ids"""


if __name__ == '__main__':
    # Everything under here except for import statements to run entire program
    # Load necessary files from datasets
    # Perform computations on the data
    # Produce an output

    # Mutates profile_id
    profile_id = set()
    run_tkinter(profile_id)

    # 1. User is prompted to enter their profile_id using code in input_data.py
    # 2. Their profile_id is passed into scrape_app_ids() in scrape_app_ids.py which returns a set of app_ids
    # 3. Convert each app_ids into Game objects with corresponding instance attributes.
    # 4. Pass user_games into create_recommendation_network()
    # 5. Decision tree
    # 6. Output/Results
