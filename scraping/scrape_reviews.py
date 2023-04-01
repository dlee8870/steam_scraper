import requests


# https://partner.steamgames.com/doc/store/getreviews

def get_json_response(app_id: int, params: dict) -> requests.models.Response.json:
    """Return the JSON response of the game reviews page
    """
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url + str(app_id), params=params)
    return response.json()


def scrape_reviews(app_id: int, n: int) -> list[dict]:
    """Return a list of n reviews (with corresponding metadata) corresponding to the app_id.
    """
    params = {
        'json': 1,
        'filter': 'all', # sorted by helpfulness
        'language': 'english',
        'day_range': 101010101010101010101010101010,
        'cursor': '*'.encode(),  # Explanation of cursor is explained in offical documentation (start of file)
        'review_type': 'positive',
        'purchase_type': 'all',
        'num_per_page': 100
    }
    reviews = []
    while n > 0:
        params['num_per_page'] = min(n, 100)  # each response cursor yields at most 100 reviews
        n -= 100
        response = get_json_response(app_id, params)
        params['cursor'] = response['cursor'].encode()
        reviews += response['reviews']
    return reviews
