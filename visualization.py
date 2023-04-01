"""CSC111 Final Project: Steam Waiter

Module Description
===============================
A module that contains classes necessary code for the visualization of the game recommendation
system's results.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Chris Oh, Ahmed Hassini, Andy Zhang, Daniel Lee
"""

from tkinter import *


def display_decision_tree():
    """Displays a pop-up window with the decision tree"""
    # Create the pop-up window
    window = Tk()
    window.title("Decision Tree")
    window.geometry("500x500")

    # Run the window
    window.mainloop()


# Call the function to display the pop-up window
display_decision_tree()


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
