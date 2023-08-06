import click
from .welp import Welp
from .click_data import ClickData
from .business_data import BusinessData
from .api.client import Client


@click.group()
def welp():
    pass


@click.command()
@click.option('--term', default='Restaurants', type=click.STRING)
@click.option('--location', type=click.STRING)
@click.option('--latitude', type=click.FLOAT)
@click.option('--longitude', type=click.FLOAT)
@click.option('--radius', default=5000, type=click.INT)
@click.option('--categories', default="", type=click.STRING)
@click.option('--locale', default="en_US", type=click.STRING)
@click.option('--limit', default=50, type=click.INT)
@click.option('--sort-by', default='best_match', type=click.STRING)
@click.option('--price', default='1,2,3', type=click.STRING)
@click.option('--attributes', default='', type=click.STRING)
@click.option('--verbose', default=False, type=click.BOOL)
def search(term, location, latitude, longitude, radius,
           categories, locale, limit, sort_by, price, attributes, verbose):
    welp = Welp()
    client = Client()

    click_data = ClickData(
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
        verbose)

    if not click_data.latitude and not click_data.longitude \
       and not click_data.location:
        lat, ln = client.geolocation.geolocate()
        click_data.set_location(lat, ln)

    bus = client.yelp.query_business_search_api(click_data)
    # print(welp.api_client.yelp.get_business('zLViW6kDKNLIYsGkBCNorg'))

    data = []
    for b in bus:
        # print(b)
        data.append(BusinessData(b))

    welp.ui.set_data(data)
    welp.ui.open_curses_ui()


welp.add_command(search)
