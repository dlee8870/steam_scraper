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
from tkinter import *
from games_network import *
from typing import Optional, Any

QUESTIONS_TO_ANSWERS = []

class DecisionTree:
    """A preset decision tree (binary tree) used to adjust scores of games from the RecommendedGameNetwork

    Each game score will be adjusted based on where it ends up in the binary tree. The games in the rightmost node at
    the end will be increased the most, and the games in the left most node will have their score increased the least.

    Note that the order of questions DOES matter. The higher up the question the higher its importance.

    We will ask the user to rank the questions.

    Preset Questions:
        1. Genre
        2. Price
        3. Release date
        4. Online component
        5. Multiplayer

    Public Instance Attributes:
        - true_branch: If the answer is positive
        - false_branch: If the answer is negative
        - question_num: Represents the index of QUESTIONS
        - games: Represents the games in this node
    """

    true_branch: Optional[DecisionTree]
    false_branch: Optional[DecisionTree]
    question_num: int
    games: set[Game]

    def __init__(self, games: set[Game], question_num: int = 0):
        self.question_num = question_num
        self.games = games
        self.true_branch = None
        self.false_branch = None


class _Questions:
    """This class represents the five questions and has seperate windows made by tkinter for each question

    The goal of this class is to get the user's answers to QUESTIONS and to rank the questions

    Public Instance Attributes:
        - window: The base window we are working with
        - genres_counter: The number of genres left for the user to choose
        - question_index: The current question that is being answered
        - genres: A set of the all possible genres in lowercase
    """

    window: Tk
    genres_counter: int
    genres: set[str]

    def __init__(self):
        self.window = Tk()
        self.genres_counter = 5
        self.question_index = 0

        # Read genres file and save into the genres attribute
        file = open("genres.txt", "r")
        self.genres = set()

        line = file.readline()
        while line != "":
            self.genres.add(line.removesuffix("\n").lower())
            line = file.readline()

    def ask_questions(self):
        """Runs the chain of functions asking the user questions"""

        self._get_genres()

    def _next_question(self, frame: Frame, user_answer: Any, question_name: str) -> None:
        """Transitions to the next question window"""
        # Clearing the screen
        frame.destroy()

        # Add answer to the list
        QUESTIONS_TO_ANSWERS.append((question_name, user_answer))

        # Calls the next question
        if question_name == "Genre":
            self._get_price()
        elif question_name == "Price":
            ...

    def _add_genre(self, genre_entry: Entry, users_genres: set[str], frame: Frame, genres_left: IntVar) -> None:
        """Tries to add genre from entry if the genre does not exist attempts to suggest a genre based on input

        Updates the genres_counter variable and mutates users_genres

        """

        response_str = StringVar()
        genre = genre_entry.get().lower()
        response_label = Label(frame, textvariable=response_str, relief=FLAT)

        if genre in users_genres:
            response_str.set(f'"{genre}" has already been selected, try another genre')
        elif genre in self.genres:
            users_genres.add(genre)
            # Creates a label that shows for a short amount of time
            response_str.set(f'Successfully added "{genre}" as a preferred genre')
            self.genres_counter -= 1
            genres_left.set(f"Genres left: {self.genres_counter}")
        else:
            # Tries to return the first relevant suggestion
            genre_suggested = False

            for g in self.genres:
                if genre in g:
                    genre_suggested = True
                    response_str.set(f'"{genre}" is not a valid genre did you mean {g}?')
                    break

            # Otherwise sends error message
            if not genre_suggested or genre == "":
                response_str.set(f'"{genre}" is not a valid genre, please try again')

        response_label.pack(side=BOTTOM)
        response_label.after(2500, lambda: response_label.destroy())

        # Clear entry
        genre_entry.delete(0, END)

        # Ends question by genre limit reached
        if self.genres_counter == 0:
            self._next_question(frame, users_genres, "Genre")

    def _get_genres(self) -> None:
        """Gets the users perferred genres"""
        frame = Frame(self.window, width=500, height=600)
        frame.pack()
        self.window.title("Preferences")
        self.window.geometry("500x600")
        self.window.resizable(False, False)

        # Question Label
        question = StringVar()
        label_question = Label(frame, textvariable=question, relief=FLAT)
        label_question.config(font=('Helvetica bold', 26))
        question.set("#1 Select at Most 5 Genres")
        label_question.pack(side=TOP)

        # Genre counter
        genres_left = IntVar()
        label_genres = Label(frame, textvariable=genres_left, relief=SUNKEN)
        label_genres.config(font=('Helvetica bold', 20))
        genres_left.set(f"Genres left: {self.genres_counter}")
        label_genres.pack(side=TOP, pady=(10, 0))

        # Search bar
        genre_label = Label(frame, text="Search for genres", font=('Helvetica bold', 14))
        genre_label.pack(side=TOP, pady=(175, 0))
        genre_entry = Entry(frame, bd=3)
        genre_entry.pack(side=TOP)

        # Enter button
        users_genres = set()
        enter_button = Button(frame, text="Enter", command=lambda: self._add_genre(genre_entry, users_genres,
                                                                                   frame, genres_left))
        enter_button.pack(pady=(15, 0))

        # Ends question by button
        next_button = Button(frame, text="Next Question", command=lambda: self._next_question(frame,
                                                                                              users_genres, "Genre"))
        next_button.pack(side=BOTTOM, pady=(160, 0))

        self.window.mainloop()

    def _add_price(self, price_entry: Entry, frame: Frame) -> None:
        """Tries to add genre from entry if the genre does not exist attempts to suggest a genre based on input

        Updates the genres_counter variable and mutates users_genres

        """

        # Catching errors when converting something that is not an integer
        try:
            price = int(price_entry.get())
            # Force ValueError for negatives
            if price < 0:
                raise ValueError
            self._next_question(frame, price, "Price")
        except ValueError:
            response_str = StringVar()
            response_str.set("Invalid entry, please enter a positive number")
            response_label = Label(frame, textvariable=response_str, relief=FLAT)
            response_label.pack(side=BOTTOM)
            response_label.after(2500, lambda: response_label.destroy())

    def _get_price(self) -> None:
        """Stores the users preferred budget"""

        frame = Frame(self.window, width=500, height=600)
        frame.pack()
        self.window.title("Preferences")
        self.window.geometry("500x600")
        self.window.resizable(False, False)

        # Question Label
        question = StringVar()
        label_question = Label(frame, textvariable=question, relief=FLAT)
        label_question.config(font=('Helvetica bold', 26))
        question.set("#2 Choose preferred cost")
        label_question.pack(side=TOP)

        # Search bar
        price_label = Label(frame, text="Enter price", font=('Helvetica bold', 14))
        price_label.pack(side=TOP, pady=(175, 0))
        price_entry = Entry(frame, bd=3)
        price_entry.pack(side=TOP)
        price_entry.update()

        # Enter button
        enter_button = Button(frame, text="Enter", command=lambda: self._next_question(frame,
                                                                                       int(price_entry.get()), "Price"))
        enter_button.pack(pady=(15, 0))

        self.window.mainloop()

def displaying_questions() -> None:
    """Displays the questions that will be used to filter the decision tree,
    asks user to adjust answers and to rank the priority of the questions

    updates the global variable QUESTIONS and USER_ANSWERS
    """

    questions = _Questions()

    questions.ask_questions()


def display_decision_tree():
    """Displays a pop-up window with the decision tree"""
    # Create the pop-up window
    window = Tk()
    window.title("Decision Tree")
    window.geometry("500x500")

    # Code for creating the decision tree and filtering games
    # Can make this while loop stall after each question or give the user the option to move to the next question
    # Maybe display the top games at the moment
    question_num = 0
    # while question_num < len(QUESTIONS):


def displaying_results():
    """Displays the results using tkinter"""


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    import doctest

    doctest.testmod()
    # python_ta.check_all(config={
    #     'extra-imports': [],  # the names (strs) of imported modules
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })
