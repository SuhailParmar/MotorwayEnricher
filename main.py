from lib.logger import Logger
from lib.rabbitmq_client import RabbitMQClient
import logging

Logger.initiate_logger()
main_logger = logging.getLogger("MotorwayEnricher Main")


def callback(ch, method, properties, body):
    # What do do when a message arrives
    pass


def main():
    mq = RabbitMQClient()
    mq.consume(callback)


if __name__ == "__main__":
    main()
