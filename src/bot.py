import tweepy
import logging
import time
import os
import random
import html
import urllib.parse
from config import create_api
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class UserListener(tweepy.StreamListener):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def on_status(self, status):
        if status.user.screen_name != self.user:
            return

        text = status.extended_tweet['full_text'] if status.truncated else status.text
        text = html.unescape(text).strip()
        logging.info('User tweeted: %s', text)

        if text.startswith('RT @') or is_url(text) or status.in_reply_to_status_id:
            logging.info('Skipping')
        else:
            if text.startswith('.@'):
                text = text[1:]

            mock = spongemock(text)
            logging.info('Tweet: %s', mock)
            tweeted = api.update_with_media(filename='mocking_spongebob.jpg', status=mock, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
            api.retweet(tweeted.id)

    def on_error(self, status_code):
        logging.error('Response status code: %s', status_code)
        return True


def is_url(string):
    try:
        parsed = urllib.parse.urlparse(string)
        return parsed.scheme and parsed.netloc
    except ValueError:
        return False


def spongemock(input_text):
    output_text = ''

    for char in input_text:
        if char.isalpha():
            if random.random() > 0.5:
                output_text += char.upper()
            else:
                output_text += char.lower()
        else:
            output_text += char

    return output_text


if __name__ == '__main__':
    api = create_api()
    handle = os.getenv("HANDLE")
    logging.info('Handle: %s', handle)
    user_id = api.lookup_users(screen_names=[handle])[0].id_str
    stream = tweepy.Stream(auth=api.auth, listener=UserListener(handle))

    while True:
        logging.info('Starting stream for user_id %s', user_id)

        try:
            stream.filter(follow=[user_id])
        except KeyboardInterrupt:
            raise
        except:
            logging.exception('Stream interrupted')