import config
import random

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key=config.CONSUMER_KEY,
    consumer_secret=config.CONSUMER_SECRET,
    token=config.TOKEN,
    token_secret=config.TOKEN_SECRET
)

yelp_client = Client(auth)

class InvalidResponseException(Exception):
    pass

def get_restaurants_by_location(location):
    response = yelp_client.search(location=location, radius_filter=config.MAX_DIST, actionlinks=True)

    print type(response)
    # TODO: Figure out error handling
    # if 'error' in response:
    #   raise InvalidResponseException

    print response.total
    restaurants = {business.name: business.rating for business \
        in response.businesses if business.rating >= config.MIN_RATING}
    print len(restaurants)

    if len(restaurants) > config.NUM_RESULTS:
        # Get a random sample of the restaurants that meet the search criteria
        selected_restaurants = random.sample(restaurants.keys(), config.NUM_RESULTS)
        restaurants = {r:restaurants[r] for r in selected_restaurants}
    print restaurants
    return restaurants

if __name__ == "__main__":
    get_restaurants_by_location(config.LOCATION)