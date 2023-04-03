"""CSC111 Final Project: Steam Waiter
Module Description
===============================
This module contains necessary code to run our entire program.
Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Chris Oh, Ahmed Hassini, Andy Zhang, Daniel Lee
"""

from input_data import run_tkinter
from scrape_app_ids import scrape_app_ids
from decision_tree import *


if __name__ == '__main__':
    # Mutates profile_id
    profile_id = list()
    run_tkinter(profile_id)

    game_app_ids_user = scrape_app_ids(profile_id[0], 6)

    app_id_to_game = {app_id: get_game_data(app_id) for app_id in game_app_ids_user}

    # This function will take some time (up to 2 minutes).
    network = create_recommendation_network(app_id_to_game)

    displaying_questions()

    top_games = display_decision_tree(network.get_games(), scrape_app_ids_all(profile_id[0]))

    # This may also take a few seconds.
    displaying_results(top_games)
