import logging

from lib.logger import Logger
from lib.utils import Utils
from lib.rabbitmq_client import RabbitMQClient
from lib.twitter_client import TwitterClient
from lib.relevance_checker import RelevanceChecker
from lib.document_clusterer import DocumentClusterer
from lib.natural_language import NaturalLanguage
from lib.exceptions import FailurePostToAPI
from lib.api_requests import APIRequests
from resources.relevant_words import RELEVANT_WORDS
from resources.tier_one_handles import T1_HANDLES

main_logger = logging.getLogger("MotorwayEnricher Main")
Logger.initiate_logger()
mq = RabbitMQClient()
rc = RelevanceChecker()
utils = Utils()
tc = TwitterClient()
nt = NaturalLanguage()
dc = DocumentClusterer()


def callback(ch, method, properties, body):
    # What do do when a message arrives
    tweet = utils.load_tweet(body)
    main_logger.info('Recieved message from Queue:{}'.format(tweet))

    timestamp = utils.parse_timestamp_with_utc(tweet["time_timestamp"])
    direction = tweet['direction']
    motorway_and_junctions, other_info =\
        rc.create_eng_keywords_from_tweet(tweet)

    tweets_in_time_period = []
    # Build query params using Capital letters and search tweets
    for j in motorway_and_junctions[1:]:
        # Search Capital M6, J25
        query = motorway_and_junctions[0] + " " + j
        tweets = tc.search_tweets_between_time_period(timestamp,
                                                      direction,
                                                      query)
        for t in tweets:
            if t not in tweets_in_time_period:
                tweets_in_time_period.append(t)

    if len(tweets_in_time_period) > 3:
        # Remove 'meaningless' words
        kws = [*motorway_and_junctions, *other_info]
        kws = nt.convert_to_lowercase(kws)
        stripped_tweets = utils.strip_words(tweets_in_time_period, kws)
        # Begin Clustering
        cluster_one = dc.main(stripped_tweets)

        data = {"extra_information": cluster_one}
        tweet_id = tweet['event_id']
        try:
            api_req = APIRequests()
            api_req.patch_to_api(tweet_id, data)
        except FailurePostToAPI as e:
            main_logger.error(e.msg)
    else:
        main_logger.info(
            "Can't create a tf-idf matrix with only {} Relevant tweets.".
            format(len(tweets_in_time_period)))


def main():
    mq.consume(callback)


if __name__ == "__main__":
    main_logger.info('Lets get this bread.')
    main()


"""
Dont look at this pls:
def t1_callback(ch, method, properties, body):
    tweet = utils.load_tweet(body)
    main_logger.info('Recieved message from Queue:{}'.format(tweet))
    timestamp = utils.parse_timestamp_with_utc(tweet["time_timestamp"])
    direction = tweet['direction']
    # Tweets which may not be related to the current incident
    T1_tweets_in_time_period = tc.poll(timestamp, direction)

    if len(T1_tweets_in_time_period) > 0:
        # Filter out unrelated tweets
        mj, other_info = rc.create_eng_keywords_from_tweet(tweet)

        kws = [*mj, *other_info]
        kws = nt.convert_to_lowercase(kws)
        T1_relevant_tweets_in_time_period = []

        for tweet in T1_tweets_in_time_period:
            if rc.is_tweet_relevant(tweet, direction):
                T1_relevant_tweets_in_time_period.ap

        T1_relevant_tweets_in_time_period = rc.find_relevant_tweets(
            T1_tweets_in_time_period, mw, junctions, directions)

        # Can only create a tfidf matrix based on >1 relevant docs
        if len(T1_relevant_tweets_in_time_period) > 1:
            kws = mw + junctions + directions  # Combine into one array
            main_logger.info(
                'Keywords from original tweet: {}'.format(kws))

            # Strip keywords out
            stripped_tweets = dc.strip_words(
                T1_relevant_tweets_in_time_period, kws)

            # Begin Clustering
            dc.main(stripped_tweets)
"""
