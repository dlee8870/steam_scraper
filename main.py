"""CSC111 Final Project: Steam Waiter
Module Description
===============================
This module contains necessary code to run our entire program.
Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Chris Oh, Ahmed Hassini, Andy Zhang, Daniel Lee
"""

from input_data import run_tkinter
from scrape_app_ids import scrape_app_ids, scrape_app_ids_all
from decision_tree import *

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

    # Mutates profile_id
    profile_id = list()
    run_tkinter(profile_id)

    game_app_ids_user = scrape_app_ids(profile_id[0], 6)

    app_id_to_game = {app_id: get_game_data(app_id) for app_id in game_app_ids_user}

    # This function will take some time
    network = create_recommendation_network(app_id_to_game)

    displaying_questions()

    top_games = display_decision_tree(network.get_games(), scrape_app_ids_all(profile_id[0]))

    displaying_results(top_games)

    # 1. User is prompted to enter their profile_id using code in input_data.py
    # 2. Their profile_id is passed into scrape_app_ids() in scrape_app_ids.py which returns a set of app_ids
    # 3. Convert each app_ids into Game objects with corresponding instance attributes.
    # 4. Pass user_games into create_recommendation_network()
    # 5. Decision tree
    # 6. Output/Results
