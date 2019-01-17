import logging

from lib.logger import Logger
from lib.utils import Utils
from lib.rabbitmq_client import RabbitMQClient
from lib.twitter_client import TwitterClient
from lib.relevance_checker import RelevanceChecker
from lib.document_clusterer import DocumentClusterer
from resources.relevant_words import RELEVANT_WORDS
from resources.tier_one_handles import T1_HANDLES

Logger.initiate_logger()

main_logger = logging.getLogger("MotorwayEnricher Main")

mq = RabbitMQClient()
rc = RelevanceChecker()
utils = Utils()
tc = TwitterClient()
dc = DocumentClusterer()


def callback(ch, method, properties, body):
    # What do do when a message arrives
    tweet = utils.load_tweet(body)
    main_logger.info('Recieved message from Queue:{}'.format(tweet))

    timestamp = utils.parse_timestamp_with_utc(tweet["time_timestamp"])
    # Tweets which may not be related to the current incident
    T1_tweets_in_time_period = tc.poll(timestamp)

    if len(T1_tweets_in_time_period) > 0:
        # Filter out unrelated tweets
        mw, junctions, directions = rc.create_eng_keywords_from_tweet(tweet)

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


def main():
    mq.consume(callback)


if __name__ == "__main__":
    main_logger.info('Lets get this bread.')
    main()
