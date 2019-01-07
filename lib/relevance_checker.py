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
            25: "twenty-five"
        }

    def construct_words_from_tweet(self, original_tweet):
        key_words = ["motorway"]

        # Extract the junction into words
        for j in original_tweet["junction"]:
            key_words.append("j" + j)
            key_words.append("junction " + j)
            key_words.append(self.number_to_words[j])

        key_words.append("m" + original_tweet["motorway"])

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

        reasons = original_tweet["reason"].split(" ")
        if len(reasons) > 0:
            key_words.append(reasons)
        else:
            for reason in reasons:
                key_words.append(reason)

        for city in original_tweet["closest_cities"]:
            key_words.append(city)

        return key_words

    def find_relevant_tweets(self, original_tweet):
        pass
