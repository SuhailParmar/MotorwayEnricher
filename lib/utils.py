from json import loads
from datetime import timedelta
import logging
utils_logger = logging.getLogger("Utils")


class Utils:

    def load_tweet(self, tweet):
        try:
            json_tweet = loads(tweet)
            return json_tweet
        except Exception as e:
            utils_logger.error('Unable to load tweet as json {}'.format(e))

    def calc_daterange_boundaries(self, timestamp, hour_offset=2):
        from_ts = timestamp - timedelta(hours=hour_offset)
        until_ts = timestamp + timedelta(hours=hour_offset)
        return from_ts, until_ts

    def within_daterange(self, new_ts, from_ts, until_ts):
        return (from_ts <= new_ts <= until_ts)
