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
import time
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
        3. Release year
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
        """Runs the chain of functions asking the user questions as well as ranking priority of questions"""

        self._get_genres()

    def _clear_window(self, frame: Frame, widgets: set[Any] | None):
        """Clears the frame of the window
        If there are extra widgets outside the frame it will erase them as well
        """

        frame.destroy()

        if widgets is not None:
            for widget in widgets:
                widget.destroy()

    def _next_question(self, frame: Frame, success_message: StringVar, user_answer: Any, question_name: str) -> None:
        """Transitions to the next question window"""
        # Success message
        response_label = Label(frame, textvariable=success_message, relief=FLAT)
        response_label.pack(side=BOTTOM)
        self.window.update()
        time.sleep(1.5)

        # Clearing the screen
        self._clear_window(frame, None)

        # Add answer to the list
        QUESTIONS_TO_ANSWERS.append((question_name, user_answer))

        # Calls the next question
        if question_name == "Genre":
            self._get_price()
        elif question_name == "Price":
            self._get_date()
        elif question_name == "Date":
            self._get_online()
        elif question_name == "Online":
            self._get_multiplayer()
        elif question_name == "Multiplayer":
            self._rank_questions()

    def _add_genre(self, genre_entry: Entry, users_genres: set[str], suggestion_str: StringVar, frame: Frame,
                   genres_left: IntVar, success_message: StringVar) -> None:
        """Tries to add genre from entry if the genre does not exist attempts to suggest a genre based on input

        Updates the genres_counter variable and mutates users_genres

        """

        response_str = StringVar(value="")
        genre = genre_entry.get().lower()
        response_label = Label(frame, textvariable=response_str, relief=FLAT)

        if genre in users_genres:
            response_str.set(f'"{genre}" has already been selected, try another genre')
            # Clear entry
            genre_entry.delete(0, END)
        elif genre in self.genres:
            users_genres.add(genre)
            # Creates a label that shows for a short amount of time
            response_str.set(f'Successfully added "{genre}" as a preferred genre')
            self.genres_counter -= 1
            success_message.set(value=f"Successfully added {5 - self.genres_counter} preferred genre(s)")
            genres_left.set(f"Genres left: {self.genres_counter}")
            # Clear entry
            genre_entry.delete(0, END)
        elif genre != "":
            # Tries to return the first relevant suggestion
            for g in self.genres:
                if genre in g and g not in users_genres:
                    response_str.set(f'"{genre}" is not a valid genre, did you mean {g}?')
                    # Adding suggestion to entry
                    suggestion_str.set(g)
                    genre_entry.icursor(END)
                    self.window.update()
                    break

        # Otherwise sends error message
        if response_str.get() == "" or genre == "":
            response_str.set(f'"{genre}" is not a valid genre, please try again')
            genre_entry.delete(0, END)

        response_label.pack(side=BOTTOM)
        response_label.after(1500, lambda: response_label.destroy())

        # Ends question by genre limit reached
        if self.genres_counter == 0:
            success_message = StringVar(value=f"Successfully added {5 - self.genres_counter} preferred genres")
            self._next_question(frame, success_message, users_genres, "Genre")

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
        suggestion_str = StringVar()
        suggestion_str.set("")
        genre_entry = Entry(frame, bd=3, textvariable=suggestion_str)
        genre_entry.pack(side=TOP)

        # Enter button
        users_genres = set()
        success_message = StringVar(value=f"Successfully added {5 - self.genres_counter} preferred genres")
        enter_button = Button(frame, text="Enter",
                              command=lambda: self._add_genre(
                                  genre_entry, users_genres, suggestion_str, frame, genres_left, success_message))
        enter_button.pack(pady=(15, 0))

        # Ends question by button
        next_button = Button(frame, text="Next Question", command=lambda: self._next_question(frame, success_message,
                                                                                              users_genres, "Genre"))
        next_button.pack(side=BOTTOM, pady=(165, 0))

        self.window.mainloop()

    def _add_price(self, price_entry: Entry, frame: Frame) -> None:
        """Tries to add price from entry"""

        # Catching errors when converting something that is not an integer
        try:
            price = int(price_entry.get())
            # Force ValueError for negatives
            if price < 0:
                raise ValueError
            else:
                success_message = StringVar(value=f"Successfully added preferred price: {price}")
                self._next_question(frame, success_message, price, "Price")
        except ValueError:
            # Clear entry
            price_entry.delete(0, END)
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
        enter_button = Button(frame, text="Enter", command=lambda: self._add_price(price_entry,
                                                                                   frame))
        enter_button.pack(pady=(15, 0))

        self.window.mainloop()

    def _add_date(self, date_entry: Entry, frame: Frame) -> None:
        """Tries to add year
        """

        # Catching errors when converting something that is not an integer
        try:
            year = int(date_entry.get())
            # Force ValueError for negatives
            if 1980 <= year <= 2023:
                success_message = StringVar(value=f"Successfully added preferred release year: {year}")
                self._next_question(frame, success_message, year, "Date")
            else:
                raise ValueError
        except ValueError:
            # Clear entry
            date_entry.delete(0, END)
            response_str = StringVar()
            response_str.set("Invalid entry, please enter a year between 1980 and 2023")
            response_label = Label(frame, textvariable=response_str, relief=FLAT)
            response_label.pack(side=BOTTOM)
            response_label.after(2500, lambda: response_label.destroy())

    def _get_date(self) -> None:
        """Stores the users preferred release date"""

        frame = Frame(self.window, width=500, height=600)
        frame.pack()
        self.window.title("Preferences")
        self.window.geometry("500x600")
        self.window.resizable(False, False)

        # Question Label
        question = StringVar()
        label_question = Label(frame, textvariable=question, relief=FLAT)
        label_question.config(font=('Helvetica bold', 26))
        question.set("#3 Choose preferred release year")
        label_question.pack(side=TOP)

        # Search bar
        date_label = Label(frame, text="Enter year", font=('Helvetica bold', 14))
        date_label.pack(side=TOP, pady=(175, 0))
        date_entry = Entry(frame, bd=3)
        date_entry.pack(side=TOP)
        date_entry.update()

        # Enter button
        enter_button = Button(frame, text="Enter", command=lambda: self._add_date(date_entry,
                                                                                  frame))
        enter_button.pack(pady=(15, 0))

        self.window.mainloop()

    def _get_online(self) -> None:
        """Stores the users preferred release date"""

        frame = Frame(self.window, width=500, height=600)
        frame.pack()
        self.window.title("Preferences")
        self.window.geometry("500x600")
        self.window.resizable(False, False)

        # Question Label
        question = StringVar()
        label_question = Label(frame, textvariable=question, relief=FLAT)
        label_question.config(font=('Helvetica bold', 26))
        question.set("#4 Do you prefer online games")
        label_question.pack(side=TOP)

        # Yes button
        online_message = StringVar(value="You prefer games that are online")
        yes_button = Button(frame, text="Yes", command=lambda: self._next_question(frame,
                                                                                   online_message, True, "Online"))
        yes_button.pack(pady=(200, 0), side=LEFT)

        # No button
        offline_message = StringVar(value="You prefer games that are offline")
        no_button = Button(frame, text="No", command=lambda: self._next_question(frame,
                                                                                 offline_message, True, "Online"))
        no_button.pack(pady=(200, 0), side=RIGHT)

        self.window.mainloop()

    def _get_multiplayer(self) -> None:
        """Stores the users preferred release date"""

        frame = Frame(self.window, width=500, height=600)
        frame.pack()
        self.window.title("Preferences")
        self.window.geometry("500x600")
        self.window.resizable(False, False)

        # Question Label
        question = StringVar()
        label_question = Label(frame, textvariable=question, relief=FLAT)
        label_question.config(font=('Helvetica bold', 26))
        question.set("#5 Do you prefer multiplayer games")
        label_question.pack(side=TOP)

        # Yes button
        online_message = StringVar(value="You prefer multiplayer games")
        yes_button = Button(frame, text="Yes", command=lambda: self._next_question(frame,
                                                                                   online_message, True, "Multiplayer"))
        yes_button.pack(pady=(200, 0), side=LEFT)

        # No button
        offline_message = StringVar(value="You do not prefer multiplayer games")
        no_button = Button(frame, text="No", command=lambda: self._next_question(frame,
                                                                                 offline_message, True, "Multiplayer"))
        no_button.pack(pady=(200, 0), side=RIGHT)

        self.window.mainloop()

    def _adjust_rank(self, curr_quest: StringVar, swap_quest: StringVar, index: int, up: bool):
        """Adjusts the rank given the current index, either increases up by on or down by 1
        if up is true swap with rank above
        otherwise swap with the rank below

        Mutates QUESTIONS_TO_ANSWERS
        """

        # Offset of change
        if up:
            offset = -1
        else:
            offset = 1

        # Swapping questions
        QUESTIONS_TO_ANSWERS[index], QUESTIONS_TO_ANSWERS[index + offset] = \
            QUESTIONS_TO_ANSWERS[index + offset], QUESTIONS_TO_ANSWERS[index]
        # Adjust labels
        curr_quest.set(f"Rank {index + 1}: {QUESTIONS_TO_ANSWERS[index][0]}")
        swap_quest.set(f"Rank {index + offset + 1}: {QUESTIONS_TO_ANSWERS[index + offset][0]}")
        self.window.update()

    def _rank_questions(self):
        """Ranks the order of the questions, the higher the question the more important it is."""

        self.window.title("Preferences")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        frame = Frame(self.window)

        # Question Label
        question = StringVar()
        label_question = Label(self.window, textvariable=question, relief=FLAT)
        label_question.config(font=('Helvetica bold', 24))
        question.set("Rank preferences by your priorities")
        label_question.pack(side=TOP, pady=(10, 100))

        frame.pack()

        # Rank 1
        question_rank_1 = StringVar()
        label_rank_1 = Label(frame, textvariable=question_rank_1, relief=FLAT)
        label_rank_1.config(font=('Helvetica bold', 18))
        question_rank_1.set("Rank 1: " + QUESTIONS_TO_ANSWERS[0][0])
        label_rank_1.grid(row=1, column=0, pady=10, padx=10)

        # Up/Down buttons for rank 1
        down_button_1 = Button(frame, text="⬇", command=lambda: self._adjust_rank(question_rank_1, question_rank_2,
                                                                                  0, False))
        down_button_1.grid(row=1, column=2, pady=10)

        # Rank 2
        question_rank_2 = StringVar()
        label_rank_2 = Label(frame, textvariable=question_rank_2, relief=FLAT)
        label_rank_2.config(font=('Helvetica bold', 18))
        question_rank_2.set("Rank 2: " + QUESTIONS_TO_ANSWERS[1][0])
        label_rank_2.grid(row=2, column=0, pady=10, padx=10)
        # Up/Down buttons for rank 2
        up_button_2 = Button(frame, text="⬆", command=lambda: self._adjust_rank(question_rank_2,
                                                                                question_rank_1, 1, True))
        up_button_2.grid(row=2, column=1, pady=10)

        down_button_2 = Button(frame, text="⬇", command=lambda: self._adjust_rank(question_rank_2,
                                                                                  question_rank_3, 1, False))
        down_button_2.grid(row=2, column=2, pady=10)

        # Rank 3
        question_rank_3 = StringVar()
        label_rank_3 = Label(frame, textvariable=question_rank_3, relief=FLAT)
        label_rank_3.config(font=('Helvetica bold', 18))
        question_rank_3.set("Rank 3: " + QUESTIONS_TO_ANSWERS[2][0])
        label_rank_3.grid(row=3, column=0, pady=10, padx=10)
        # Up/Down buttons for rank 3
        up_button_3 = Button(frame, text="⬆", command=lambda: self._adjust_rank(question_rank_3,
                                                                                question_rank_2, 2, True))
        up_button_3.grid(row=3, column=1, pady=10)

        down_button_3 = Button(frame, text="⬇", command=lambda: self._adjust_rank(question_rank_3,
                                                                                  question_rank_4, 2, False))
        down_button_3.grid(row=3, column=2, pady=10)

        # Rank 3
        question_rank_4 = StringVar()
        label_rank_4 = Label(frame, textvariable=question_rank_4, relief=FLAT)
        label_rank_4.config(font=('Helvetica bold', 18))
        question_rank_4.set("Rank 4: " + QUESTIONS_TO_ANSWERS[3][0])
        label_rank_4.grid(row=4, column=0, pady=10, padx=10)
        # Up/Down buttons for rank 3
        up_button_4 = Button(frame, text="⬆", command=lambda: self._adjust_rank(question_rank_4,
                                                                                question_rank_3, 3, True))
        up_button_4.grid(row=4, column=1, pady=10)

        down_button_4 = Button(frame, text="⬇", command=lambda: self._adjust_rank(question_rank_4,
                                                                                  question_rank_5, 3, False))
        down_button_4.grid(row=4, column=2, pady=10)

        # Rank 3
        question_rank_5 = StringVar()
        label_rank_5 = Label(frame, textvariable=question_rank_5, relief=FLAT)
        label_rank_5.config(font=('Helvetica bold', 18))
        question_rank_5.set("Rank 5: " + QUESTIONS_TO_ANSWERS[4][0])
        label_rank_5.grid(row=5, column=0, pady=10, padx=10)
        # Up/Down buttons for rank 3
        up_button_5 = Button(frame, text="⬆", command=lambda: self._adjust_rank(question_rank_5,
                                                                                question_rank_4, 4, True))
        up_button_5.grid(row=5, column=1, pady=10)

        # Ends the questionnaire
        next_button = Button(self.window, text="Get Recommendations", command=lambda: self._clear_window(
            frame, {label_question, next_button}))
        next_button.pack(side=BOTTOM, pady=(0, 100))

        self.window.mainloop()


def displaying_questions() -> None:
    """Displays the questions that will be used to filter the decision tree,
    asks user to adjust answers and to rank the priority of the questions

    updates the global variable QUESTIONS and USER_ANSWERS
    """

    questions = _Questions()

    questions.ask_questions()


def display_decision_tree(window: Tk):
    """Displays a pop-up window with the decision tree"""
    # Create the pop-up window
    window = Tk()
    window.title("Decision Tree")
    window.geometry("500x500")

    # Code for creating the decision tree and filtering games
    # Can make this while loop stall after each question or give the user the option to move to the next question
    # Maybe display the top games at the moment
    # while question_num < len(QUESTIONS):


def displaying_results():
    """Displays the results using tkinter with the scores out of 10.

    """


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
