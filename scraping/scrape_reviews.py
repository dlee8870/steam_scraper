import requests


def get_json_response(appid: int, params: dict) -> requests.models.Response.json:
    """Return the json of the game review page
    """
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url + str(appid), params=params, headers={'User-Agent': 'Mozilla/5.0'})
    return response.json()


def get_reviews(app_id: int, n: int) -> list[dict]:
    """Return a list of n reviews (with corresponding metadata) corresponding to the app_id.
    """
    reviews = []
    cursor = '*'
    params = {
        'json': 1,
        'filter': 'all',
        'language': 'english',
        'day_range': 9223372036854775807,  # all time
        'review_type': 'all',
        'purchase_type': 'all'
    }

    while n > 0:  # Each json response only gets 100 reviews, so this is a way around it if n > 100
        params['cursor'] = cursor.encode()
        params['num_per_page'] = min(100, n)
        n -= 100

        response = get_json_response(app_id, params)
        cursor = response['cursor']
        reviews += response['reviews']

        if len(response['reviews']) < 100:
            break

    return reviews
