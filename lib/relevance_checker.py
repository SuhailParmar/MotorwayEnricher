import logging

rl_logger = logging.getLogger("RelevanceChecker")


class RelevanceChecker:

    def __init__(self):
        self.number_to_words = {
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            14: "fourteen",
            15: "fifteen",
            25: "twenty-five"
        }

    def construct_words_from_tweet(self, original_tweet, key_words):
        """
        Convert important data in the tweet into strings
        returns an array of strings
        """
        mw_number = str(original_tweet["motorway"])
        mw = "m" + mw_number

        # First element in the KEYWORDS must be the motorway
        key_words.insert(0, mw)
        key_words.append("motorway")

        # Extract the junction into words
        for i, j in enumerate(original_tweet["junction"]):
            key_words.insert((i+1), "j" + str(j))

            key_words.append("junction " + str(j))
            try:
                key_words.append(self.number_to_words[j])
            except KeyError as e:
                rl_logger.warn(
                    'Junction {} cannot be converted into a word'.format(e))

        key_words.append("m" + str(original_tweet["motorway"]))

        if original_tweet["direction"] == "n":
            key_words.append("northbound")
            key_words.append("north")
            key_words.append("n/bound")
        elif original_tweet["direction"] == "e":
            key_words.append("eastbound")
            key_words.append("east")
            key_words.append("e/bound")
        elif original_tweet["direction"] == "s":
            key_words.append("southbound")
            key_words.append("south")
            key_words.append("s/bound")
        elif original_tweet["direction"] == "w":
            key_words.append("westbound")
            key_words.append("west")
            key_words.append("w/bound")

        # TODO neaten this
        reasons = original_tweet["reason"].split(" ")
        if len(reasons) > 0:
            for reason in reasons:
                key_words.append(reason)
        else:
            key_words.append(reasons)

        for city in original_tweet["closest_cities"]:
            cities = city.split(" ")
            for c in cities:
                key_words.append(c)

        return key_words

    def create_eng_keywords_from_tweet(self, original_tweet):
        """
        Generate english keywords from the original tweet
        Important information: motorway, junctions, direction
        """
        motorway = []
        mw_number = str(original_tweet["motorway"])
        motorway.append("m" + mw_number)

        junctions = []
        for j in original_tweet["junction"]:
            junctions.append("j" + str(j))

            junctions.append("junction " + str(j))
            try:
                junctions.append("junction " + self.number_to_words[j])
            except KeyError as e:
                rl_logger.warn(
                    'Junction {} cannot be converted into a word'.format(e))

        directions = []

        if original_tweet["direction"] == "n":
            directions.append("northbound")
            directions.append("north")
            directions.append("n/bound")
        elif original_tweet["direction"] == "e":
            directions.append("eastbound")
            directions.append("east")
            directions.append("e/bound")
        elif original_tweet["direction"] == "s":
            directions.append("southbound")
            directions.append("south")
            directions.append("s/bound")
        elif original_tweet["direction"] == "w":
            directions.append("westbound")
            directions.append("west")
            directions.append("w/bound")

        return (motorway, junctions, directions)

    def find_relevant_tweets(self, tweets, motorway, junctions, directions):
        """
        Only choose a subset of tweets which are about:
        The motorway in question
        The junction in question
        Direction is currently irrelevant
        """

        relevant_tweets = []

        for tweet in tweets:
            rl_logger.debug('Relevance checking: {}'.format(tweet))
            if motorway[0] not in tweet:
                rl_logger.debug('Tweet is not about the M6.')
                continue

            junction_flag = False
            for junction in junctions:
                if junction in tweet:
                    junction_flag = True

            if not junction_flag:
                rl_logger.debug(
                    'Tweet is not about junction(s) {}.'.format(junctions))
                continue

            # TODO Maybe have 2 tiers based on direction??
            relevant_tweets.append(tweet)

        rl_logger.info('Found {0} RELEVANT tweets!'.format(
            len(relevant_tweets)))

        if len(relevant_tweets) > 0:
            for i, relevant_tweet in enumerate(relevant_tweets):
                rl_logger.info(str(i) + ') ' + relevant_tweet)

        return relevant_tweets
