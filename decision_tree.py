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
from typing import Optional, Any
from queue import Queue
import math
import time
from tkinter import *
import random
from games_network import *


# This is a list of tuples where the first element is the question and the second element is the user's answer
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

    def __init__(self, games: set[Game], user_games: Optional[set[Game]] = None, question_num: int = 0) -> None:
        self.question_num = question_num
        if user_games is not None:
            self.games = games - user_games
        else:
            self.games = set()
        self.true_branch = None
        self.false_branch = None

    def generate_preset_decision_tree(self) -> None:
        """Generates teh decision tree."""

        queue = Queue()
        queue.put_nowait(self)

        while not queue.empty():
            subtree = queue.get_nowait()

            # Addign its subtrees
            subtree.true_branch = DecisionTree(set(), question_num=subtree.question_num + 1)
            subtree.false_branch = DecisionTree(set(), question_num=subtree.question_num + 1)

            # Our binary tree is of height 6, so we only need to create more subtrees if it at most height 4
            if subtree.question_num + 1 < 5:
                queue.put_nowait(subtree.true_branch)
                queue.put_nowait(subtree.false_branch)

    def filter_by_genre(self) -> tuple[int, int]:
        """Filters the games to the true_branch if it matches the user's genre preference,
        otherwise moves it to the false_branch

        True if the game contains at least one of the users preferred genres or if user's preferred genre is false,
        False otherwise

        returns a tuple of the number of positive and negative games

        Preconditions:
            - QUESTION_TO_ANSWERS[self.question_num][0] = "Genre"
        """

        user_genres = QUESTIONS_TO_ANSWERS[self.question_num][1]
        num_positive_games, num_negative_games = 0, 0

        for game in self.games:

            if user_genres == set() or any(user_genre in game.genres for user_genre in user_genres):
                self.true_branch.games.add(game)
                num_positive_games += 1
            else:
                self.false_branch.games.add(game)
                num_negative_games += 1

        return num_positive_games, num_negative_games

    def filter_by_price(self) -> tuple[int, int]:
        """Filters the games to the true_branch if it matches the user's price preference,
        otherwise moves it to the false_branch

        True if the price simillarity is at least 50%
        False otherwise

        returns a tuple of the number of positive and negative games

        Preconditions:
            - QUESTION_TO_ANSWERS[self.question_num][0] = "Price"
        """
        k = 0.05  # tuning parameter
        user_price = QUESTIONS_TO_ANSWERS[self.question_num][1]
        num_positive_games, num_negative_games = 0, 0

        for game in self.games:
            x = abs(game.price - user_price)
            price_similratiy = math.exp(-k * x)

            if price_similratiy >= 0.5:
                self.true_branch.games.add(game)
                num_positive_games += 1
            else:
                self.false_branch.games.add(game)
                num_negative_games += 1

        return num_positive_games, num_negative_games

    def filter_by_date(self) -> tuple[int, int]:
        """Filters the games to the true_branch if it matches the user's date preference,
        otherwise moves it to the false_branch

        The range of the dates is from 1980 to 2023

        True if the sbdolute difference the dates is less than or equal to 7
        False otherwise

        returns a tuple of the number of positive and negative games

        Preconditions:
            - QUESTION_TO_ANSWERS[self.question_num][0] = "Date"
        """

        user_date = QUESTIONS_TO_ANSWERS[self.question_num][1]
        num_positive_games, num_negative_games = 0, 0

        for game in self.games:
            diff = abs(game.release_date - user_date)

            if diff <= 7:
                self.true_branch.games.add(game)
                num_positive_games += 1
            else:
                self.false_branch.games.add(game)
                num_negative_games += 1

        return num_positive_games, num_negative_games

    def filter_by_online(self) -> tuple[int, int]:
        """Filters the games to the true_branch if it matches the user's online preference,
        otherwise moves it to the false_branch

        This value is already either true or false

        True if the games online state matches the user's online preference
        False otherwise

        returns a tuple of the number of positive and negative games

        Preconditions:
            - QUESTION_TO_ANSWERS[self.question_num][0] = "Online"
        """
        user_online = QUESTIONS_TO_ANSWERS[self.question_num][1]
        num_positive_games, num_negative_games = 0, 0

        for game in self.games:

            if user_online == game.online:
                self.true_branch.games.add(game)
                num_positive_games += 1
            else:
                self.false_branch.games.add(game)
                num_negative_games += 1

        return num_positive_games, num_negative_games

    def filter_by_multiplayer(self) -> tuple[int, int]:
        """Filters the games to the true_branch if it matches the user's multiplayer preference,
        otherwise moves it to the false_branch

        This value is already either true or false

        True if the games multiplayer state matches the user's multiplayer preference
        False otherwise

        returns a tuple of the number of positive and negative games

        Preconditions:
            - QUESTION_TO_ANSWERS[self.question_num][0] = "Multiplayer"
        """
        user_multiplayer = QUESTIONS_TO_ANSWERS[self.question_num][1]
        num_positive_games, num_negative_games = 0, 0

        for game in self.games:

            if user_multiplayer == game.multiplayer:
                self.true_branch.games.add(game)
                num_positive_games += 1
            else:
                self.false_branch.games.add(game)
                num_negative_games += 1

        return num_positive_games, num_negative_games


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
    question_index: int

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Preferences")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.genres_counter = 5
        self.question_index = 0

        # Read genres file and save into the genres attribute
        file = open("genres.txt", "r")
        self.genres = set()

        line = file.readline()
        while line != "":
            self.genres.add(line.removesuffix("\n").lower())
            line = file.readline()

    def ask_questions(self) -> None:
        """Runs the chain of functions asking the user questions as well as ranking priority of questions
        """

        self._get_genres()

    def _clear_window(self, frame: Frame, widgets: set[Any] | None) -> None:
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
        else:
            self._rank_questions()

    def _add_genre(self, genre_entry: Entry, users_genres: set[str], suggestion_str: StringVar, frame: Frame,
                   genres_left: StringVar, success_message: StringVar) -> None:
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

        # Question Label
        question = StringVar()
        label_question = Label(frame, textvariable=question, relief=FLAT)
        label_question.config(font=('Helvetica bold', 26))
        question.set("#1 Select at Most 5 Genres")
        label_question.pack(side=TOP)

        # Genre counter
        genres_left = StringVar()
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
                                                                                 offline_message, False, "Multiplayer"))
        no_button.pack(pady=(200, 0), side=RIGHT)

        self.window.mainloop()

    def _adjust_rank(self, curr_quest: StringVar, swap_quest: StringVar, index: int, up: bool) -> None:
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

    def _rank_questions(self) -> None:
        """Ranks the order of the questions, the higher the question the more important it is."""

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
        next_button = Button(self.window, text="Get Recommendations", command=self._desrtroy_window())
        next_button.pack(side=BOTTOM, pady=(0, 100))

        self.window.mainloop()

    def _desrtroy_window(self) -> None:
        """Destroys the window"""
        self.window.destroy()


def displaying_questions() -> Tk:
    """Displays the questions that will be used to filter the decision tree,
    asks user to adjust answers and to rank the priority of the questions

    updates the global variable QUESTIONS_TO_ANSWERS
    """

    questions = _Questions()

    questions.ask_questions()


def destroy_frame(frame: Frame) -> None:
    """Destroys the frame"""

    frame.destroy()


def _display_stats_for_question(frame: Frame, question: str, positive_per: float,
                                negative_per: float, get_results: bool) -> list[[tuple[Game, int]]]:
    """Displays the stats of the current question on the given frame

    Pauses the decision tree computation until the user clicks the continue button which destroys the frame.

    Returns the top games
    """

    # Current filter
    curr_question = StringVar()
    label_curr_question = Label(frame, textvariable=curr_question, relief=FLAT)
    label_curr_question.config(font=('Helvetica bold', 20))
    curr_question.set(f"Results of Filtering by {question} Preference")
    label_curr_question.pack(side=TOP, pady=60)

    # The results
    positive_str = StringVar()
    label_positive_results = Label(frame, textvariable=positive_str, relief=SOLID)
    label_positive_results.config(font=('Helvetica bold', 18))
    positive_str.set(f"Percentage of Games That Match your {question} Prefence: {positive_per}")
    label_positive_results.pack(side=TOP, pady=(75, 10))

    negative_str = StringVar()
    label_negative_results = Label(frame, textvariable=negative_str, relief=SOLID)
    label_negative_results.config(font=('Helvetica bold', 18))
    negative_str.set(f"Percentage of Games That did Not Match your {question} Prefence: {negative_per}")
    label_positive_results.pack(side=TOP)

    # Continue button
    if get_results:
        button_text = "Get Results"
    else:
        button_text = "Continue"

    continue_button = Button(frame, text=button_text, command=lambda: destroy_frame(frame))
    continue_button.pack(side=BOTTOM, pady=(0, 100))

    frame.mainloop()


def display_decision_tree(window: Tk, games: set[Game], user_games: set[Game]) -> list[tuple[Game, int]]:
    """Displays a pop-up window with the decision tree

    Note we do not need a visited set since this is a binary tree

    Returns the top fivve games and the window
    """
    print("Done")
    decision_tree = DecisionTree(games, user_games)
    window.title("Finding Games You Will Like")
    window.geometry("500x600")
    window.resizable(False, False)
    frame = Frame(window)
    frame.pack()

    # Header Label
    header = StringVar()
    label_header = Label(window, textvariable=header, relief=FLAT)
    label_header.config(font=('Helvetica bold', 26))
    header.set("Filtering Games")
    label_header.pack(side=TOP)

    window.update()

    # Creates the decision tree
    decision_tree.generate_preset_decision_tree()

    queue = Queue()
    queue.put_nowait(decision_tree)

    order_of_games = []

    display_counter = 1
    total_games = len(decision_tree.games)

    # The stats per question this will be reset each question
    num_positive_games_per_q, num_negative_game_per_q = 0, 0

    while not queue.empty():
        subtree = queue.get_nowait()
        question = QUESTIONS_TO_ANSWERS[subtree.question_num][0]

        # When we are filtering for a new questions show the results to the window of the last question
        if subtree.question_num == display_counter:
            percentage_of_positives = num_positive_games_per_q / total_games
            percentage_of_negatives = num_negative_game_per_q / total_games
            last_question = QUESTIONS_TO_ANSWERS[display_counter - 1][0]
            _display_stats_for_question(frame, last_question, percentage_of_positives, percentage_of_negatives, False)

            num_positive_games_per_q, num_negative_game_per_q = 0, 0
            display_counter += 1

        # Filter games comapring their attributes to the answer given by the user
        if question == "Genre":
            results = subtree.filter_by_genre()
            num_positive_games_per_q += results[0]
            num_negative_game_per_q += results[1]
        elif question == "Price":
            results = subtree.filter_by_price()
            num_positive_games_per_q += results[0]
            num_negative_game_per_q += results[1]
        elif question == "Date":
            results = subtree.filter_by_date()
            num_positive_games_per_q += results[0]
            num_negative_game_per_q += results[1]
        elif question == "Online":
            results = subtree.filter_by_online()
            num_positive_games_per_q += results[0]
            num_negative_game_per_q += results[1]
        else:
            results = subtree.filter_by_multiplayer()
            num_positive_games_per_q += results[0]
            num_negative_game_per_q += results[1]

        # If the next subtrees have a question to ask
        if (subtree.question_num + 1) < 5:
            queue.put_nowait(subtree.false_branch)
            queue.put_nowait(subtree.true_branch)
        else:
            # The end result of the games when they have filtered into the last subtree
            # Notice that since we are adding the false branch first this will give us
            # the order from least similar to most similar

            order_of_games.append(subtree.false_branch.games)
            order_of_games.append(subtree.true_branch.games)

    # Transition here to get results destroy header label here display the last results as well here
    percentage_of_positives = num_positive_games_per_q / total_games
    percentage_of_negatives = num_negative_game_per_q / total_games
    last_question = QUESTIONS_TO_ANSWERS[4][0]
    _display_stats_for_question(frame, last_question, percentage_of_positives, percentage_of_negatives, True)

    # Get the results
    top_five = _get_results(order_of_games)

    return top_five


def _get_results(order_of_games: list[set[Game]]) -> list[tuple[Game, int]]:
    """Based on the ordering of the games get the top three games combining likeability score and
    the ordering done by the decision tree.

    If there is a tie we take the game higher up in the order
    To break another tie take the game with the higher likeability score
    Otherwise keep the game that was already in the top 3

    returns the top five games
    """
    # Getting the starting 3, note that there will always be atleast 1000 games in teh network
    # thus there must atleast one order which contains at least 3 games in it
    starting_5 = random.choice(order_of_games).copy()
    while len(starting_5) < 5:
        starting_5 = random.choice(order_of_games).copy()

    # The pop method for set removes and return random elements this is why I made a copy, so it does not mutate
    top_five = [starting_5.pop() for _ in range(0, 5)]

    for order in range(0, len(order_of_games)):
        for game in order_of_games[order]:
            _compare_top_five(top_five, game, order + 1)

    return top_five


def _compare_top_five(top_five: list[tuple[Game, int]], game: Game, order: int) -> None:
    """Comapres the game witht the top_five if it has a higher score it will mutate top_five

    The higher the index in top_three the higher the game score

    The first element of the tuple is the game and the second element is the order of the game
    The higher the order the more similar the game is to the user's preferences
    """

    for i in range(0, 5):
        if _compare_games((game, order), top_five[i]):
            if i == 0:
                top_five[0] = (game, order)
            else:
                top_five[i - 1], top_five[i] = top_five[i], top_five[i - 1]
        else:
            break


def _compare_games(game1: tuple[Game, int], game2: tuple[Game, int]) -> bool:
    """Given two game and its order return true if game 1 should be higher up

    Note max order is 64

    To compute the user preference score it will be on a scale of 0 - 5 where the order determined its scaling

    Break ties as mentioned in _get_results
    """

    game1_score = game1[0].likeability + (game1[1] / 64) * 5
    game2_score = game2[0].likeability + (game2[1] / 64) * 5

    if game1_score > game2_score:
        return True
    elif game1_score == game2_score and game1[1] > game2[1]:
        return True
    elif game1_score == game2_score and game1[1] == game2[1] and game1[0].likeability > game2[0].likeability:
        return True
    else:
        return False


def displaying_results(window: Tk, top_games: list[tuple[Game, int]]) -> None:
    """Displays the results using tkinter with the scores out of 10 and other information.
    """

    window.title("Serving Your Games!")
    window.geometry("500x600")
    window.resizable(False, False)

    # Header Label
    header = StringVar()
    label_header = Label(window, textvariable=header, relief=FLAT)
    label_header.config(font=('Helvetica bold', 26))
    header.set(f"Your top 5 games")
    label_header.pack(side=TOP)

    frame1 = Frame(window)
    frame1.pack()

    # Game 1
    game1, preference_score_1 = top_games[4][0], top_games[4][1] / 64
    game1_stats = StringVar()
    label_game1 = Label(frame1, textvariable=header, relief=FLAT)
    label_game1.config(font=('Helvetica bold', 18))
    game1_stats.set(f"Game #1: {game1.name}"
                    f"Genres: {game1.genres}"
                    f"Price: {game1.price}"
                    f"Release Year: {game1.release_date}"
                    f"Online: {game1.online}"
                    f"Multiplayer: {game1.multiplayer}"
                    f"General Likeability Score: {round((game1.likeability / 3) * 100, 1)}"
                    f"User Likeability Score: {round(preference_score_1 * 100, 1)}"
                    f"Total Score: {round(((game1.likeability + preference_score_1 * 5) / 8)) * 100, 1}")
    label_game1.grid(row=0, column=0)

    # Game 2
    game2, preference_score_2 = top_games[3][0], top_games[3][1] / 64
    game2_stats = StringVar()
    label_game2 = Label(frame1, textvariable=header, relief=FLAT)
    label_game2.config(font=('Helvetica bold', 18))
    game2_stats.set(f"Game #2: {game2.name}"
                    f"Genres: {game2.genres}"
                    f"Price: {game2.price}"
                    f"Release Year: {game2.release_date}"
                    f"Online: {game2.online}"
                    f"Multiplayer: {game2.multiplayer}"
                    f"General Likeability Score: {round((game2.likeability / 3) * 100, 1)}"
                    f"User Likeability Score: {round(preference_score_2 * 100, 1)}"
                    f"Total Score: {round(((game2.likeability + preference_score_2 * 5) / 8)) * 100, 1}")
    label_game2.grid(row=0, column=1)

    # Game 3
    game3, preference_score_3 = top_games[2][0], top_games[2][1] / 64
    game3_stats = StringVar()
    label_game3 = Label(frame1, textvariable=header, relief=FLAT)
    label_game3.config(font=('Helvetica bold', 18))
    game3_stats.set(f"Game #3: {game3.name}"
                    f"Genres: {game3.genres}"
                    f"Price: {game3.price}"
                    f"Release Year: {game3.release_date}"
                    f"Online: {game3.online}"
                    f"Multiplayer: {game3.multiplayer}"
                    f"General Likeability Score: {round((game3.likeability / 3) * 100, 1)}"
                    f"User Likeability Score: {round(preference_score_3 * 100, 1)}"
                    f"Total Score: {round(((game3.likeability + preference_score_3 * 5) / 8)) * 100, 1}")
    label_game3.grid(row=0, column=1)

    # Game 4
    game4, preference_score_4 = top_games[1][0], top_games[1][1] / 64
    game4_stats = StringVar()
    label_game4 = Label(frame1, textvariable=header, relief=FLAT)
    label_game4.config(font=('Helvetica bold', 18))
    game4_stats.set(f"Game #4: {game4.name}"
                    f"Genres: {game4.genres}"
                    f"Price: {game4.price}"
                    f"Release Year: {game4.release_date}"
                    f"Online: {game4.online}"
                    f"Multiplayer: {game4.multiplayer}"
                    f"General Likeability Score: {round((game4.likeability / 3) * 100, 1)}"
                    f"User Likeability Score: {round(preference_score_4 * 100, 1)}"
                    f"Total Score: {round(((game4.likeability + preference_score_4 * 5) / 8)) * 100, 1}")
    label_game4.grid(row=1, column=0)

    # Game 5
    game5, preference_score_5 = top_games[0][0], top_games[0][1] / 64
    game5_stats = StringVar()
    label_game5 = Label(frame1, textvariable=header, relief=FLAT)
    label_game5.config(font=('Helvetica bold', 18))
    game5_stats.set(f"Game #5: {game5.name}"
                    f"Genres: {game5.genres}"
                    f"Price: {game5.price}"
                    f"Release Year: {game5.release_date}"
                    f"Online: {game5.online}"
                    f"Multiplayer: {game5.multiplayer}"
                    f"General Likeability Score: {round((game5.likeability / 3) * 100, 1)}"
                    f"User Likeability Score: {round(preference_score_5 * 100, 1)}"
                    f"Total Score: {round(((game5.likeability + preference_score_5 * 5) / 8)) * 100, 1}")
    label_game5.grid(row=1, column=1)

    window.mainloop()


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    import doctest

    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['typing', 'queue', 'math', 'time', 'tkinter', 'games_network', 'random'],
        'allowed-io': [],
        'disable': ['wildcard-import', 'too-many-arguments', 'unnecessary-lambda', 'too-many-locals',
                    'too-many-statements'],
        'max-line-length': 120
    })
