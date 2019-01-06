import twitter
import logging
import lib.config as config

th_logger = logging.getLogger("TwitterClient")


class TwitterClient:
    """
    The client will search tweets via the
    key words
    """

    def __init__(self):
        self.api = self.authenticate()

    def authenticate(self):
        logging.debug('Authenticating against the Twitter API...')
        return twitter.Api(consumer_key=config.twitter_api_key,
                           consumer_secret=config.twitter_api_secret,
                           access_token_key=config.twitter_at_token,
                           access_token_secret=config.twitter_at_secret)
