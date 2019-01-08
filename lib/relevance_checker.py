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
        key_words.append("motorway")

        # Extract the junction into words
        for j in original_tweet["junction"]:
            key_words.append("j" + str(j))
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
        elif original_tweet["direction"] == "e":
            key_words.append("eastbound")
            key_words.append("east")
        elif original_tweet["direction"] == "s":
            key_words.append("southbound")
            key_words.append("south")
        elif original_tweet["direction"] == "w":
            key_words.append("westbound")
            key_words.append("west")

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

    def find_relevant_tweets(self, key_words, tweets):
        """
        Determines if the tweets gathered are relevant
        @key_words: Array of strings
        @tweets: Array of payloads from tweets.
        """
        for i, tweet in enumerate(tweets):
            remove = True
            for kw in key_words:
                if kw in tweet:
                    remove = False
            if remove:
                tweets.remove(tweet)

        return tweets
