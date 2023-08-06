
import requests
from .google.geolocation import Geolocation
from .yelp.business import BusinessSearch


class Client:
    def __init__(self):
        self.session = requests.session()
        self.yelp = BusinessSearch(self)
        self.geolocation = Geolocation(self)
