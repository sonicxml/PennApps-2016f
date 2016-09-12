import flask
import config
import yelp_handler
import json
import requests

slack_posturl = "https://slack.com/api/chat.postMessage"
slack_reacturl = "https://slack.com/api/reactions.add"

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
    restaurants = yelp_handler.get_restaurants_by_location(location)
    return restaurants

@app.route('/slack', methods=['POST'])
def generate_response():
    form_info = flask.request.form

    if config.API_TOKEN != form_info['token']:
        raise InvalidTokenException

    # First, parse args and find the restaurants
    passed_args = form_info['text']
    channel = form_info['channel_id']
    restaurants = get_restaurants_from_yelp(config.LOCATION)
    # Next, send POST request with list of restaurants for Slack
    post_data = {
        'response_type': 'in_channel',
        'text': "Here's a list of restaurants to choose from today!",
        'attachments': [{'title': r, 'text': 'Rating: ' + \
                            str(restaurants[r])} for r in restaurants.keys()],
        'token': config.API_TOKEN,
        'channel': channel
    }

    # post_data['response_type'] = 'in_channel'
    # post_data['text'] = "Here's a list of restaurants to choose from today!"
    # post_data['attachments'] = [{'title': r, 'text': 'Rating: ' + \
    #     str(restaurants[r])} for r in restaurants.keys()]
    # post_data['token'] = config.API_TOKEN
    # post_data['channel'] = channel

    post_response = requests.post(slack_posturl, data=post_data)

    # Finally, add poll reactions
    # Heavily inspired by SimplePoll for Slack
    emoji_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', \
        'eight', 'nine', 'keycap_ten']
    for i in xrange(min(len(emoji_names), len(restaurants))):
        reaction_data = {
            'token': config.API_TOKEN,
            'name': emoji_names[i],
            'channel': channel,
            'timestamp': post_response['ts']
        }
        requests.post(slack_reacturl, data=reaction_data)

    return ''

def main():
    app.run(host='0.0.0.0', port='9999', threaded=True)

if __name__ == '__main__':
    main()