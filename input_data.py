"""CSC111 Final Project: Steam Waiter

Module Description
===============================
A module that contains classes necessary code for the inputting data
for visualization of results.

Copyright and Usage Information
===============================
This file is Copyright (c) 2023 Daniel Lee, Andy Zhang, Chris Oh, Ahmed Hassini
"""

from __future__ import annotations
from tkinter import *

root = Tk()
root.geometry("500x500")
root.title("Welcome to Steam Waiter")

input_pf = Entry(root, width=50)
input_pf.place(relx=0.5, rely=0.2, anchor='n')

def run_tkinter():
    """Run the Tkinter application"""

    label = Label(root, text="Enter Steam Profile", font=('Arial', 18))
    label.place(rely=0.1, relx=0.34)

    # Enter button to input data
    button = Button(root, text='Find games!', font=('Arial', 18), command=store_data)
    button.place(relx=0.37, rely=0.3)

    # Default text in the input box
    input_pf.insert(0, "Enter info here")

    # Run the window
    root.mainloop()


def store_data():
    """Store the data inputed in the textbox into a variable"""
    steam_id = input_pf.get()

    # Perhaps call functions to create decision tree


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
