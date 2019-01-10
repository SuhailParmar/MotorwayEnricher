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

    def find_relevant_tweets(self, key_words, tweets, bound=5):
        """
        Determines if the tweets gathered are relevant places into
        three arrays depending on 'importance'
        @key_words: Array of strings
        @tweets: Array of tokenized payloads from tweets.
        """
        relevant_tweets_t1 = []  # Directly mention the motorway and junction
        relevant_tweets_t2 = []  # Directly mention the motorway but different junction

        for tweet in tweets:
            if key_words[0] not in tweet:
                # The motorway in question
                continue

            if (key_words[1]) in tweet or (key_words[2] in tweet):
                # Check the junction
                relevant_tweets_t1.append(tweet)
                continue

            # First 2 aray positions have been checked
            for i, kw in enumerate(key_words, 2):
                if kw in tweet:
                    relevant_tweets_t2.append(tweet)
                    break

        if len(relevant_tweets_t1) < bound:
            return relevant_tweets_t1 + relevant_tweets_t2

        rl_logger.info("{} tweets are being ignored due to the bound param.".format(
            len(relevant_tweets_t2)))
        return relevant_tweets_t1
