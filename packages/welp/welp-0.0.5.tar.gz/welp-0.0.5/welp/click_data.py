

class ClickData:
    def __init__(
            self,
            term,
            location,
            latitude,
            longitude,
            radius,
            categories,
            locale,
            limit,
            sort_by,
            price,
            attributes,
            verbose):
        self.term = term.replace(' ', '+')
        self.location = location.replace(' ', '+') if location else None
        self.latitude = latitude
        self.longitude = longitude
        self.term = term
        self.radius = radius
        self.categories = categories
        self.locale = locale
        self.limit = limit
        self.sort_by = sort_by
        self.price = price
        self.attributes = attributes
        self.verbose = verbose

    def set_location(self, lat, ln):

        self.latitude = lat
        self.longitude = ln
