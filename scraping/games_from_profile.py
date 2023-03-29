import requests


def get_games_list_response(profile_id: int = 76561198023414915) -> requests.models.Response.json:
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
    response = requests.get(url + f'4957E3F30616447A483A7DBA9F26172E&steamid={str(profile_id)}&format=json')
    return response.json()


def top_n_played(profile_id: int = 76561198023414915, n: int = 10):
    games = get_games_list_response(profile_id)['response']['games']
    sorted_by_playtime = sorted(games, key=lambda g: g['playtime_forever'], reverse=True)
    return sorted_by_playtime[0:n]
