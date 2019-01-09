from lib.logger import Logger
from lib.utils import Utils
from lib.rabbitmq_client import RabbitMQClient
from lib.twitter_client import TwitterClient
from lib.relevance_checker import RelevanceChecker
from resources.relevant_words import RELEVANT_WORDS
from resources.tier_one_handles import T1_HANDLES
import logging

Logger.initiate_logger()
main_logger = logging.getLogger("MotorwayEnricher Main")

mq = RabbitMQClient()
rc = RelevanceChecker()
utils = Utils()
tc = TwitterClient()


def callback(ch, method, properties, body):
    # What do do when a message arrives
    tweet = utils.load_tweet(body)

    main_logger.debug('Recieved message from Queue:{}'.format(tweet))

    relevant_words = RELEVANT_WORDS[tweet["reason"]]
    key_words = rc.construct_words_from_tweet(tweet, relevant_words)

    main_logger.debug(
        'Constructed keywords from original tweet: {}'.format(key_words))

    timestamp = utils.parse_timestamp_with_utc(tweet["time_timestamp"])

    T1_relevant_tweets_in_time_period = []
    for handle in T1_HANDLES:
        tweets = tc.poll_tweets_between_time_period(handle, timestamp)
        main_logger.debug('Found {0} tweets:\n{1}'.format(len(tweets), tweets))
        tweets = rc.find_relevant_tweets(key_words, tweets)
        main_logger.debug('Found {0} RELEVANT tweets from @{1}:\n{2}'.format(len(tweets), handle, tweets))

        for tweet in tweets:
            T1_relevant_tweets_in_time_period.append(tweet)

    main_logger.info('Found {0} RELEVANT tweets in total.'.format(len(T1_relevant_tweets_in_time_period)))
    pass


def main():
    mq.consume(callback)


if __name__ == "__main__":
    main()