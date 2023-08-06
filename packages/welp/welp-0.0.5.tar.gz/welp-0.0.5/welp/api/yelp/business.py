import os
from urllib.parse import quote

API_KEY = os.environ['YELP_API_KEY']
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
REVIEWS_PATH = '/reviews'
SEARCH_LIMIT = 20


class BusinessSearch:
    def __init__(self, client):
        self.client = client

    def request(self, host, path, api_key, url_params=None):
        url_params = url_params or {}
        url = f"{host}{quote(path.encode('utf8'))}"
        headers = {
            'Authorization': 'Bearer %s' % api_key,
        }

        # print(u'Querying {0} ...'.format(url))

        response = self.client.session.request(
            'GET', url, headers=headers, params=url_params)

        return response.json()

    def get_business(self, business_id):
        """Query the Business API by a business ID.

        Args:
            business_id (str): The ID of the business to query.

        Returns:
            dict: The JSON response from the request.
        """
        business_path = BUSINESS_PATH + business_id

        return self.request(API_HOST, business_path, API_KEY)

    def get_business_reviews(self, business_id):
        """Query the Business API by a business ID.

        Args:
            business_id (str): The ID of the business to query.

        Returns:
            dict: The JSON response from the request.
        """
        business_path = BUSINESS_PATH + business_id + REVIEWS_PATH

        return self.request(API_HOST, business_path, API_KEY)

    def query_business_search_api(self, url_params):
        """Queries the API by the input values from the user.
        Args:
            term (str): The search term to query.
            location (str): The location of the business to query.
        """
        response = self.request(API_HOST, SEARCH_PATH,
                                API_KEY, url_params=url_params.__dict__)

        # print(response)

        return response.get('businesses')
