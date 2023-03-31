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
    reviews = []
    params = {
        'json': 1,
        'filter': 'all',
        'language': 'all',
        'day_range': 99999999999999999,  # all time
        'review_type': 'all',
        'purchase_type': 'all',
        'cursor': '*'
    }

    while n > 0:  # Explanation of cursor is explained in documentation above (start of file)
        params['cursor'] = params['cursor'].encode()
        params['num_per_page'] = min(100, n)
        n -= 100

        response = get_json_response(app_id, params)
        reviews += response['reviews']
        #
        # if len(response['reviews']) < 100:
        #     break

    return reviews
