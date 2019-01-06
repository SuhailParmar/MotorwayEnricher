from json import loads
import logging
utils_logger = logging.getLogger("Utils")


class Utils:

    def load_tweet(self, tweet):
        try:
            json_tweet = loads(tweet)
            return json_tweet
        except Exception as e:
            utils_logger.error('Unable to load tweet as json {}'.format(e))
