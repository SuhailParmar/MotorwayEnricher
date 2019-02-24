import twitter
import logging
from datetime import datetime
from dateutil.parser import parse
import lib.config as config
from lib.utils import Utils
from lib.natural_language import NaturalLanguage
from lib.relevance_checker import RelevanceChecker
from resources.tier_one_handles import T1_HANDLES

th_logger = logging.getLogger("TwitterClient")
ut = Utils()
nt = NaturalLanguage()
rc = RelevanceChecker()


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
        TODO convert to using maxid
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

    def search_tweets_between_time_period(self,
                                          original_tweet_timestamp,
                                          original_direction,
                                          query_params):
        """
        Search for tweets fulfilling the query params
        original_tweet_timestamp 2019-01-25T18:00:45
        query_params M6 J3 #// Space seperated values
        """
        # timestamp = ut.parse_timestamp_with_utc(original_tweet_timestamp)
        # Get the boundaries of the timerange 4 hours greater
        from_timestamp, until_timestamp = ut.calc_daterange_boundaries(
            original_tweet_timestamp, from_offset=0, to_offset=4)

        # Twitter API require date in form YYYY/MM/DD
        from_date = from_timestamp.strftime('%Y-%m-%d')
        tweets_in_date_range = []

        th_logger.info(
            'Globally searching tweets during period {0} - {1} under query {2}'.format(
                from_timestamp, until_timestamp, query_params))

        max_id = None  # Prevent retrieving the same tweet
        continue_polling = True  # Stop retrieving new tweets

        while continue_polling:
            tweets = self.api.GetSearch(count=25, term=query_params,
                                        since=from_date,
                                        max_id=max_id)

            if max_id is not None and(tweets[len(tweets) - 1].id == max_id):
                # Ensure the polled tweets arent repeats
                continue_polling = False
                break

            if len(tweets) == 0:
                th_logger.info(
                    "Retrieved no tweets relating to the original tweet.")
                continue_polling = False
                break

            max_id = tweets[len(tweets) - 1].id
            # Reverse inspect the timeline
            for index in range(len(tweets)-1, 0, -1):
                tweet = tweets[index]
                th_logger.info("Insepecting tweet text\n{0}\nAt {1}".format(
                    tweet.text, tweet.created_at))
                # Created At timestamp
                tweet_timestamp = parse(tweet.created_at)
                in_range = ut.is_day_in_range(
                    tweet_timestamp, from_timestamp, until_timestamp)

                if in_range is 0:
                    th_logger.info("Tweet is in range")
                    relevant_tweet =\
                        rc.is_tweet_relevant(tweet, original_direction)

                    if not relevant_tweet:
                        continue

                    # Ignore duplicates
                    if relevant_tweet in tweets_in_date_range:
                        th_logger.info(
                            'Skipping duplicate tweet: {}'.format(
                                relevant_tweet))
                        continue

                    tweets_in_date_range.append(relevant_tweet)

                elif in_range is 1:
                    # Re-Poll
                    th_logger.info("Tweet is ABOVE range. Repolling")
                    break
                elif in_range is 2:
                    # The tweet is earlier than the lower bound
                    # Stop polling but continue to validate tweets
                    th_logger.info("Tweet is BELOW range.")
                    continue_polling = False

        return tweets_in_date_range

