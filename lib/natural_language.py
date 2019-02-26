from nltk import word_tokenize


class NaturalLanguage:

    def tokenize(self, sentence):
        return word_tokenize(sentence)

    def convert_to_lowercase(self, values):

        if not isinstance(values, list):
            return values.lower()

        for i, value in enumerate(values):
            try:
                lc_value = value.lower()
                values[i] = lc_value
            except Exception as e:
                print("Couldnt convert" + e)
        return values
