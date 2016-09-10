import flask
import config

app = flask.Flask(__name__)

@app.route('/')
def index():
    return '83'

@app.route('/slack', methods=['POST'])
def get_restaurants_from_yelp():
	# Talk to yelp
	return restaurants