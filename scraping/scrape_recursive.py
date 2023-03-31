import requests
import pandas as pd
from bs4 import BeautifulSoup
import scrape_games


class User:
    profile_id: str | int
    similar_games: list[dict]

    def __init__(self, profile_id: str | int) -> None:
        if isinstance(profile_id, str):
            self.profile_id = convert_to_64bit(profile_id)
        else:
            self.profile_id = profile_id

    def scrape_similar(self):
        top_n = scrape_games.top_n_played(self.profile_id, 10)
        df = pd.DataFrame(top_n)
        df.to_csv('top_n_played.csv')


def convert_to_64bit(profile_id: str = 'star_19642') -> int:
    url = f'https://steamid.net/?q={profile_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    converted = soup.find('input', {'id': 'results_steamid64'})
    return int(converted['value'])
