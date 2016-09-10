import config

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key=config.CONSUMER_KEY,
    consumer_secret=config.CONSUMER_SECRET,
    token=config.TOKEN,
    token_secret=config.TOKEN_SECRET
)

yelp_client = Client(auth)


def get_restaurants_by_location(location):
	response = yelp_client.search(location)
	print response

	for business in response.businesses:
		print business.name
		print business.rating


if __name__ == "__main__":
	get_restaurants_by_location(config.LOCATION)