import twitter
import logging
from datetime import datetime
from dateutil.parser import parse
import lib.config as config
from lib.utils import Utils
from lib.natural_language import NaturalLanguage
from resources.tier_one_handles import T1_HANDLES

th_logger = logging.getLogger("TwitterClient")
ut = Utils()


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

    def poll_tweets_between_time_period(self, handle, timestamp):
        """
        Handle: Twitter Account Name @SuhailParmar
        Timestamp: Time want to see if they tweeted at that time
        """
        n = 5  # Number of tweets to grab at one time
        i = 0  # Index of the tweets array
        max_tweets = 100  # Maximum number of tweets to scrape
        from_timestamp, until_timestamp = ut.calc_daterange_boundaries(
            timestamp, hour_offset=2)
        timeline_in_date_range = []  # Finished
        nt = NaturalLanguage()
        th_logger.info('Looking for tweets for user {0} in  period {1} - {2}'.format(
            handle, from_timestamp, until_timestamp))

        while i < max_tweets:
            timeline = self.api.GetUserTimeline(screen_name=handle, count=i+n)
            unvalidated_tweets = timeline[i:]

            for ind, tweet in enumerate(unvalidated_tweets):
                tweet_timestamp = parse(tweet.created_at)
                th_logger.debug(
                    'Validating if {0} is in the bounds of {1} - {2}'.format(
                        tweet_timestamp, from_timestamp, until_timestamp))

                if ut.within_daterange(
                        tweet_timestamp, from_timestamp, until_timestamp):
                    # tweet.text is the payload of the tweet
                    lowercase_tweet = nt.convert_to_lowercase(tweet.text)
                    timeline_in_date_range.append(lowercase_tweet)
                    continue

                elif tweet_timestamp < from_timestamp:
                    # If the account has been polled passed the from timestamp boundary
                    # Then quit
                    th_logger.debug(
                        'Unable to find a tweet in the date range in {} tweets'.format(i))
                    # An empty return
                    return timeline_in_date_range

                elif len(timeline_in_date_range) > 0:
                    return timeline_in_date_range

            th_logger.debug(
                'Havent found a tweet in the date range in {} tweets.'.format(i))
            i += n

        th_logger.info(
            'Didnt find a tweet in the date range in {} tweets'.format(i))

        return timeline_in_date_range

    def poll(self, timestamp):
        """
        Poll between user provided timestamps for
        Tier 1 tweeters
        """
        T1_tweets_in_time_period = []

        for handle in T1_HANDLES:
            th_logger.info(
                'Searching handle @{0}\n\n'.format(handle))

            tweets = self.poll_tweets_between_time_period(handle, timestamp)
            th_logger.info(
                'Found {0} tweets in that time period by @{1}.'.format(
                    len(tweets), handle))

            if len(tweets) == 0:
                continue

            th_logger.debug('**Tweets Found in time period**')
            for tweet in tweets:
                th_logger.debug('{}'.format(tweet))
                T1_tweets_in_time_period.append(tweet)

        return T1_tweets_in_time_period

    def search_tweets(self, original_tweet_timestamp, params):
        """
        params M6 J3 #// Space seperated values
        date 'yyyy:mm:dd'
        COuldnt get max_id to work
        """
        timestamp = ut.parse_timestamp_with_utc(original_tweet_timestamp)
        # Only get tweets 2 hours after reported incident
        from_timestamp, until_timestamp = ut.calc_daterange_boundaries(
            timestamp, from_offset=0, to_offset=2)

        th_logger.info(
            'Looking for global tweets during period {0} - {1}'.format(
                from_timestamp, until_timestamp))

        raw_query = "q=" + params

        """
        Search tweets which are in a specific date boundary
        If the last tweet is in bounds we need to search more tweets as well
        If the last tweet is above upper bound search more tweets
        if last tweet is under lower bound we need to stop searching
        """

        nt = NaturalLanguage()
        valid_results = []
        continue_polling = True  # Poll as many tweets as possible
        maxid = None
        while continue_polling:
            # Get 20 Tweets each iteration

            if maxid is None:
                results = self.api.GetSearch(raw_query=raw_query,
                                             until=from_timestamp.isoformat(),
                                             )
            else:
                results = self.api.GetSearch(raw_query=raw_query,
                                             until=from_timestamp.isoformat(),
                                             max_id=maxid
                                             )

            # Check if the last tweet is under boundary
            last_tweet = results[len(results) - 1]
            last_tweet_timestamp = parse(last_tweet.created_at)

            in_range = ut.is_day_in_range(
                last_tweet_timestamp, from_timestamp, until_timestamp)

            if in_range is 1:
                # Keep polling
                maxid = (last_tweet.id -1)
                continue

            elif in_range is 2:
                continue_polling = False

            for tweet in results:
                if tweet.user.screen_name in T1_HANDLES:
                    # Ignore tweets already grabbed
                    continue

                tweet_timestamp = parse(tweet.created_at)
                if(ut.within_daterange(
                        tweet_timestamp, from_timestamp, until_timestamp)):

                    lowercase_tweet = nt.convert_to_lowercase(tweet.text)
                    valid_results.append(lowercase_tweet)

        return valid_results
