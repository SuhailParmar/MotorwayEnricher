from lib.logger import Logger
from lib.utils import Utils
from lib.rabbitmq_client import RabbitMQClient

import logging

Logger.initiate_logger()
main_logger = logging.getLogger("MotorwayEnricher Main")
mq = RabbitMQClient()
utils = Utils()


def callback(ch, method, properties, body):
    # What do do when a message arrives
    tweet = utils.load_tweet(body)
    main_logger.debug('Recieved message from Queue:{}'.format(tweet))
    pass


def main():
    mq.consume(callback)


if __name__ == "__main__":
    main()
