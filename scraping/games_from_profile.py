from bs4 import BeautifulSoup
import requests


def get_app_ids(profile_id: int = 'DadFox1'):
    cookies = {'birthtime': '283993201', 'mature_content': '1'}  # Bypasses age checks for games
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = {'username': 'steam_scraping_temp', 'password': 'JANSF958^%195ma'}
    post = "https://help.steampowered.com/en/login/"

    with requests.session() as s:
        s.post(post, data=data)  # log us in
        r = s.get(url=f'https://steamcommunity.com/profiles/{profile_id}/games/?tab=all',
                  headers=headers,
                  cookies=cookies)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
