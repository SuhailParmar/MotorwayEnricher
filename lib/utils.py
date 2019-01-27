from json import loads
from datetime import timedelta
from datetime import timezone
from dateutil.parser import parse
import logging
utils_logger = logging.getLogger("Utils")


class Utils:

    def load_tweet(self, tweet):
        try:
            json_string = loads(tweet)
            json_tweet = loads(json_string)
            return json_tweet
        except Exception as e:
            utils_logger.error('Unable to load tweet as json {}'.format(e))
            exit(1)

    def calc_daterange_boundaries(self, timestamp, hour_offset=2,
                                  from_offset=None, to_offset=None):

        if from_offset is not None and to_offset is not None:
            from_ts = timestamp - timedelta(hours=from_offset)
            until_ts = timestamp + timedelta(hours=to_offset)

        else:
            from_ts = timestamp - timedelta(hours=hour_offset)
            until_ts = timestamp + timedelta(hours=hour_offset)

        return from_ts, until_ts

    def within_daterange(self, new_ts, from_ts, until_ts):
        return (from_ts <= new_ts <= until_ts)

    def is_day_in_range(self, new_ts, from_ts, until_ts):
        """
        If the timestamp is after the until ts then continue polling
        If the timestamp is before the from ts then stop polling
        """
        # 5:10 10th , 2 hours  3:10 (from) 7:10 (to)
        if new_ts > until_ts:
            # Poll results again
            return 1

        if new_ts < from_ts:
            # Stop polling
            return 2

        return 0  # (from_ts <= new_ts <= until_ts)

    def parse_timestamp_with_utc(self, utc_unaware_timestamp):
        """
        utc_unaware_timestamp: tweet["time_timestamp"]
        """
        # TODO Fix this in the tweet_converter?
        # The timestamp provided has no knowledge of the timezone
        # Z is the quickest way to identify a UTC timestamp.
        utc_aware_timestamp = utc_unaware_timestamp + 'Z'
        utc_aware_timestamp_datetime = parse(utc_aware_timestamp)
        return utc_aware_timestamp_datetime
