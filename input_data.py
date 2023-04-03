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
from tkinter import messagebox

root = Tk()
root.geometry("500x600")
root.title("Welcome to Steam Waiter")

input_pf = Entry(root, width=50)
input_pf.place(relx=0.5, rely=0.2, anchor='n')

r = IntVar()
r.get()


def run_tkinter():
    """Run the Tkinter application"""

    label = Label(root, text="Steam Waiter: Serving your game", font=('Arial', 18))
    label.place(rely=0.1, relx=0.22)

    # Enter button to input data
    button = Button(root, text='Find games!', font=('Arial', 18), command=store_data)
    button.place(relx=0.36, rely=0.3)

    # Information button
    info_button = Button(root, text='I', font=('Times New Roman', 18), command=display_info)
    info_button.place(relx=0.8, rely=0.8)

    Radiobutton(root, text='Default 64-bit profile', variable=r, value=1).place(rely=0.5, relx=0.35)
    Radiobutton(root, text='Custom Profile', variable=r, value=2).place(rely=0.6, relx=0.35)

    # Default text in the input box
    input_pf.insert(0, "Enter info here")

    # Run the window
    root.mainloop()


def display_info():
    """Give instructions on how to operate menu"""
    messagebox.showinfo("Tutorial", "First, select your choice of input (64-bit or custom), and then fill out the box")


def store_data():
    """Store the data inputed in the textbox into a variable"""
    # If the input is 64-bit all int profile
    if r.get() == 1:
        all_int_64_prof = input_pf.get()
        # If length of 64 bit != 17 or if every the input is not all integers
        if len(all_int_64_prof) != 17 or all(letter.isnumeric() for letter in all_int_64_prof) is False:
            messagebox.showerror("Error", "Invalid input")
        else:
            # Perhaps call Decision Tree here
            ...
    # IF the input is a custom profile input
    else:
        custom_prof = input_pf.get()
        if custom_prof.isalpha() is True:
            messagebox.showerror("Error", "Invalid input")
        else:
            # Perhaps call Decision Tree here
            ...


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
