from lib.utils import Utils
from lib.natural_language import NaturalLanguage
import logging

rl_logger = logging.getLogger("RelevanceChecker")


class RelevanceChecker:

    def __init__(self):

        self.nl = NaturalLanguage()

        self.directions = {
            "a": ["anti-clockwise"],
            "c": ["clockwise", "c/w"],
            "e": ["eastbound", "e/bound", "east"],
            "n": ["northbound", "n/bound", "north"],
            "s": ["southbound", "s/bound", "south"],
            "w": ["westbound", "w/bound", "west"],
        }

    def create_eng_keywords_from_tweet(self, original_tweet):
        """
        Generate english keywords from the original tweet
        Important information: motorway, junctions
        Other less-important info: reasons, cities
        return ([motorway, junctions**], [other_info])
        """
        motorway_and_junction = []
        mw_number = str(original_tweet["motorway"])
        motorway_and_junction.append("M" + mw_number)
        for j in original_tweet["junction"]:
            motorway_and_junction.append("J" + str(j))

        # Directions
        other_info = []
        if original_tweet["direction"] == "n":
            other_info.append("northbound")
            other_info.append("north")
            other_info.append("n/bound")
        elif original_tweet["direction"] == "e":
            other_info.append("eastbound")
            other_info.append("east")
            other_info.append("e/bound")
        elif original_tweet["direction"] == "s":
            other_info.append("southbound")
            other_info.append("south")
            other_info.append("s/bound")
        elif original_tweet["direction"] == "w":
            other_info.append("westbound")
            other_info.append("west")
            other_info.append("w/bound")
        elif original_tweet["direction"] == "a":
            other_info.append("anti-clockwise")
        elif original_tweet["direction"] == "c":
            other_info.append("clockwise")

        reasons_strings = original_tweet["reason"].split(" ")
        if isinstance(reasons_strings, list):
            for r in reasons_strings:
                other_info.append(r)
        else:
            other_info.append(reasons_strings)

        for c in original_tweet["closest_cities"]:
            split = c.split(" ")
            for v in split:
                if v is not '/':
                    other_info.append(v.lower())

        rl_logger.debug("Constructed Keywords:\n{0}{1}".format(
            motorway_and_junction, other_info))
        return (motorway_and_junction, other_info)

    def is_tweet_relevant(self, tweet, original_direction):
        rl_logger.info("Checking relevance of\n{0}".format(tweet.text))

        if tweet.user.screen_name is "@epsomcanine":
            rl_logger.info('Skipping Dog tweet: {}'.format(tweet.text))
            return False

        # The tweet's timestamp is in bounds of from_timestamp and until_timestamp
        lowercase_tweet = self.nl.convert_to_lowercase(tweet.text)
        lowercase_tweet = Utils.strip_link_from_tweet(lowercase_tweet)

        # ignore retweets
        if lowercase_tweet[0] == 'r' and lowercase_tweet[1] == 't':
            rl_logger.info('Skipping Retweet: {}'.format(tweet.text))
            return False

        if not self.is_relevant_direction(original_direction, tweet):
            rl_logger.info('Tweet is not about direction {}'.format(
                original_direction))
            return False

        rl_logger.info('** Keeping tweet:\n {}'.format(tweet.text))
        return lowercase_tweet

    def is_relevant_direction(self, original_direction, tweet):
        if original_direction is "a":
            # clockwise is in 'anti-clockwise' so search
            # entire tweet for "anti-clockwise"
            return self.directions["a"][0] in tweet

        for k, v in self.directions.items():
            if k is not original_direction:
                for value in v:
                    if value in tweet:
                        return False

        return True
