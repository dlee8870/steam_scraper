from bs4 import BeautifulSoup
import requests
from requests import session


def get_app_ids(profile_id: int | str = 'DadFox1'):
    cookies = {'birthtime': '283993201',
               'mature_content': '1'}

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    if isinstance(profile_id, str):
        response = requests.get(url=f'https://steamcommunity.com/profiles/{profile_id}/games/?tab=all',
                                headers=headers,
                                cookies=cookies)
    else:
        response = requests.get(url=f'https://steamcommunity.com/id/{profile_id}/games/?tab=all',
                                headers=headers,
                                cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup
