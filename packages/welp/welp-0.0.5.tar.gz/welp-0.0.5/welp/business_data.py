

'''
{'id': 'zLViW6kDKNLIYsGkBCNorg',
'alias': 'paesano-ristorante-italiano-san-jose',
'name': 'Paesano Ristorante Italiano',
'image_url': 'https://s3-media4.fl.yelpcdn.com/bphoto/0K_JiyyYtQDw1gw8xY2YWQ/o.jpg',
'is_closed': False,
'url': 'https://www.yelp.com/biz/paesano-ristorante-italiano-san-jose?adjust_creative=Tb7mKIyLJPzAUf1fWI9E9g&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=Tb7mKIyLJPzAUf1fWI9E9g',
'review_count': 1019,
'categories': [{'alias': 'italian', 'title': 'Italian'}],
'rating': 4.0, 'coordinates': {'latitude': 37.336166540678, 'longitude': -121.89867135144},
'transactions': ['delivery'],
'price': '$$',
'location': {'address1': '350 W Julian St', 'address2': 'Ste 1', 'address3': '', 'city': 'San Jose', 'zip_code': '95110', 'country': 'US', 'state': 'CA', 'display_address': ['350 W Julian St', 'Ste 1', 'San Jose, CA 95110']},
'phone': '+14082179327',
'display_phone': '(408) 217-9327',
'distance': 484.37802455489407}
'''


class BusinessData:
    def __init__(self, data):
        self.id = data['id']
        self.alias = data['alias']
        self.name = data['name']
        self.image_url = data['image_url']
        self.is_closed = data['is_closed']
        self.url = data['url']
        self.display_url = data['url'].split('?')[0]
        self.review_count = data['review_count']
        self.categories = data['categories']
        self.transactions = data['transactions']
        self.price = data['price']
        self.location = data['location']
        self.display_location = " ".join(data['location']['display_address'])
        self.phone = data['phone']
        self.display_phone = data['display_phone']
        self.rating = data['rating']
        self.distance = data['distance']

        self.convert_price()
        self.convert_categories()

    def __repr__(self):
        return self.name

    def __str__(self):
        return " ".join([self.id, self.name])

    def extend_details(self, data):
        self.hours = data['hours']
        self.photos = data['photos']
        self.coordinates = data['coordinates']
        # yelp why is this an array???
        self.is_open_now = data['hours'][0]['is_open_now']

    def get_full_printable(self):
        return [
            self.name,
            "",
            '{} 🌟 {} reviews {}'.format(self.rating, self.review_count, self.display_price),
            "",
            '📞 {}'.format(self.display_phone),
            '🌐 {}'.format(self.display_url),
            '📫 {}'.format(self.display_location),
            '',
            "{} {}".format(", ".join([x['title'] for x in self.categories]), self.display_categories),
            "",
            'Open Now' if self.is_open_now else 'Closed',
            # "",         
            # "{}".format(self.reviews[0]['text'])
        ]

    def get_printable(self):
        return [
            self.name,
            '{}🌟({}) {} {}'.format(self.rating, self.review_count,
                                   self.display_price,
                                   self.display_categories),
            self.display_location,
            self.display_url,
            ""
        ]

    def convert_price(self):
        self.display_price = '💲' * len(self.price)

    def convert_categories(self):
        ret = ""
        category_to_emoji = {
            'seafood': '🦞',
            'burgers': '🍔',
            'tacos': '🌮',
            'foodtrucks': '🚛',
            'italian': '🍝',
            'german': '',
            'bars': '🍻',
            'beergardens': '🍻',
            'mexican': '🌮',
            'venues': '',
            'fishnchips': '🦞',
            'newmexican': '🌮',
            'greek': '🥙',
            'mediterranean': '🥙',
            'cajun': '🦐',
            'chicken_wings': '🍗',
            'chickenshop': '🍗',
            'tapasmallplates': '🍢',
            'tapas': '🍢',
            'wine_bars': '🍷',
            'whiskybars': '🥃',
            'shanghainese': '🍜',
            'cantonese': '🥮',
            'chinese': '🥮',
            'coffee': '☕',
            'hkcafe': '🥮',
            'bbq': '🥩',
            'southern': '🥩',
            'cambodian': '',
            'persian': '',
            'japanese': '🍣',
            'hotpot': '🍲',
            'diyfood': '',
            'noodles': '🍜',
            'vegan': '',
            'panasian': '',
            'asianfusion': '',
            'lounges': '',
            'soup': '🍲',
            'ramen': '🍜',
            'japacurry': '🍛',
            'brewpubs': '🍺',
            'hawaiian': '🌴',
            'tikibars': '🌴',
            'brasseries': '',
            'musicvenues': '',
            'food_court': '',
            'carribean': '',
            'tradamerican': '',
            'pizza': '🍕',
            'hotdog': '🌭',
            'hotdogs': '🌭',
            'pubs': '🍺',
            'gastropubs': '🍺',
            'french': '',
            'kebab': '🍢',
            'halal': '',
            'asianfusion': '',
            'vietnamese': '🍜',
            'cocktailbars': '',
            'korean': '🍚',
            'poke': '',
            'steak': '🥩',
            'bubbletea': '🍹',
            'himalayan': '',
            'newamerican': '',
            'breakfast_brunch': '🥓',
            'salads': '🥗',
            'thai': '',
        }

        for c in self.categories:
            if c['alias'] in category_to_emoji:
                ret += category_to_emoji[c['alias']]

        self.display_categories = ret
