import requests
from bs4 import BeautifulSoup
import games_from_profile
import reviews_from_game


class User:
    profile_id: str | int

    def __init__(self, profile_id: str | int):
        if isinstance(profile_id, str):
            self.profile_id = convert_to_64bit(profile_id)

        else:
            self.profile_id = profile_id

    def scrape_similar(self):
        topn = games_from_profile.top_n_played(self.profile_id, 10)
        for t in topn:
            reviews_from_game.get_n_reviews(t['appid'], 5)


def convert_to_64bit(profile_id: str = 'star_19642') -> int:
    url = f'https://steamid.net/?q={profile_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    converted = soup.find('input', {'id': 'results_steamid64'})
    return converted['value']
