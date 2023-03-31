import requests
from bs4 import BeautifulSoup
from scrape_games import scrape_games
from scrape_reviews import scrape_reviews
import pandas as pd


class UserScrape:
    """A class representing the root user to start from, with the specified scraping settings.
    ...
    """
    profile_id: str | int
    games: list[dict]
    n: int  # Determines how many games to scrape from this user.
    recurse_n: int  # Determines how many games to scrape from other users
    d: int  # Depth of recursion, the smaller, the more "similar"

    def __init__(self, profile_id: str | int, n: int, d: int) -> None:
        if isinstance(profile_id, str):
            self.profile_id = convert_to_64bit(profile_id)
        else:
            self.profile_id = profile_id
        self.n = n
        self.d = d

    def scrape(self):
        games = scrape_games(self.profile_id, self.n)
        scrape_recursive_games(games)


def scrape_recursive_games(games: list[dict]):
    for game in games:
        ...


def convert_to_64bit(profile_id: str) -> int:
    url = f'https://steamid.net/?q={profile_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    converted = soup.find('input', {'id': 'results_steamid64'})
    return int(converted['value'])
