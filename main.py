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
from scrape_game_data import get_game_data

# Note to self: Need to split up program into the following files according to assignment page:
#   - Reading data (done)
#   - Computing on data
#   - Display of data
#   - main.py (has a main block to run entire program from start to finish.)


if __name__ == '__main__':
    # Everything under here except for import statements to run entire program
    # Load necessary files from datasets
    # Perform computations on the data
    # Produce an output

    # 1. User is prompted to enter their profile_id using code in input_data.py
    profile_id = 76561198976283119
    # 2. Their profile_id is passed into scrape_app_ids() in scrape_app_ids.py which returns a set of app_ids
    app_ids = list(scrape_app_ids(profile_id, 10))
    # 3. Convert each app_ids into Game objects with corresponding instance attributes.
    user_games = {}

    for app_id in app_ids:
        game = get_game_data(app_id)
        user_games[game] = app_id

    # 3. Pass user_games into create_recommendation_network()
    games_network = create_recommendation_network(user_games)

    # 4. Decision tree
    # 5. Output/Results

