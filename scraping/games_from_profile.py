from bs4 import BeautifulSoup
import requests


def get_app_ids(profile_id: int | str):
    if isinstance(profile_id, str):
        response = requests.get(url=f'https://steamcommunity.com/profiles/{profile_id}/games/?tab=all',
                                headers={'User-Agent': 'Mozilla/5.0'})
    else:
        response = requests.get(url=f'https://steamcommunity.com/id/{profile_id}/games/?tab=all',
                                headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(response.text, 'html.parser')
    app_id = soup.find(class_='search_result_row')['data-ds-appid']


return app_id
