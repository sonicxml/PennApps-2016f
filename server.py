import flask
import config

app = flask.Flask(__name__)

class InvalidTokenException(Exception):
	pass

@app.errorhandler(InvalidTokenException)
def handle_invalid_token(error):
	abort(403)

@app.route('/')
def index():
    return 'SuperSwagSauce(TM) Productions'

def get_restaurants_from_yelp(location):
	# Talk to yelp
	return restaurants

@app.route('/slack', methods=['POST'])
def generate_response():
	form_info = flask.request.form

	if config.API_TOKEN != form_info['token']:
		raise InvalidTokenException

	# First, parse args and find the restaurants
	passed_args = form_info['text']
	restaurants = get_restaurants_from_yelp(config.LOCATION)
	# Next, create poll for people to vote on the restaurants

def main():



if __name__ == '__main__':
	main()