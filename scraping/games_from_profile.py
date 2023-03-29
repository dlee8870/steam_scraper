import requests


def get_games_list_response(profile_id: int) -> requests.models.Response.json:
    """Returns the JSON response of the games list page for the user corresponding to profile_id.
    """
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
    response = requests.get(url + f'4957E3F30616447A483A7DBA9F26172E&steamid={str(profile_id)}&format=json')
    return response.json()


def top_n_played(profile_id: int, n: int) -> list[dict]:
    """Returns a list of the n most played games for the user corresponding to profile_id.
    """
    games = get_games_list_response(profile_id)['response']['games']
    sorted_by_playtime = sorted(games, key=lambda g: g['playtime_forever'], reverse=True)
    return sorted_by_playtime[0:n]
