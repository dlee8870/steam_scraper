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
import requests


def run_tkinter(profile_id: list) -> None:
    """Run the Tkinter application"""
    root = Tk()
    root.geometry("500x600")
    root.resizable(False, False)
    root.title("Welcome to Steam Waiter")

    input_pf = Entry(root, width=50)
    input_pf.place(relx=0.5, rely=0.2, anchor='n')

    r = IntVar()
    r.get()

    label = Label(root, text="Steam Waiter: Serving your game", font=('Arial', 18))
    label.place(rely=0.1, relx=0.22)

    # Enter button to input data
    button = Button(root, text='Find games!', font=('Arial', 18), command=lambda: store_data(profile_id, input_pf,
                                                                                             r, root))
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


def display_info() -> None:
    """Give instructions on how to operate menu"""
    messagebox.showinfo("Tutorial", "First, select your choice of input (64-bit or custom), "
                                    "then fill out the input box with your profile ID.")


def store_data(profile_id: list, input_pf: Entry, r: IntVar, root: Tk) -> None:
    """Store the data inputed in the textbox into profile_id by a mutating"""

    # If the input is 64-bit all int profile
    if r.get() == 1:
        all_int_64_prof = input_pf.get()
        # If length of 64 bit != 17 or if every the input is not all integers
        if len(all_int_64_prof) != 17 or all(letter.isnumeric() for letter in all_int_64_prof) is False:
            messagebox.showerror("Error", "Invalid input")
        else:
            # Change from str to int
            all_int_64_prof = int(all_int_64_prof)
            profile_id.append(all_int_64_prof)
    # IF the input is a custom profile input
    else:
        custom_prof = input_pf.get()
        if custom_prof.isalpha() is True:
            messagebox.showerror("Error", "Invalid input")
        else:
            profile_id.append(convert_to_64bit(custom_prof))

    root.destroy()


def convert_to_64bit(profile_id: str) -> int:
    """Helper function for scrape_app_ids().
    Given a custom SteamID, this function returns the 64-bit representation of the SteamID.

    Preconditions:
        - profile_id is a custom SteamID

    >>> convert_to_64bit('star_19642')
    76561199000093113
    """
    url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
    params = {
        'key': '4957E3F30616447A483A7DBA9F26172E',
        'vanityurl': profile_id
    }
    response = requests.get(url, params).json()
    return int(response['response']['steamid'])


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'requests'],
        'allowed-io': [],
        'disable': ['wildcard-import'],
        'max-line-length': 120
    })
