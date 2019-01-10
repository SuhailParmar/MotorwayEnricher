from nltk import word_tokenize


class NaturalLanguage:

    def tokenize(self, sentence):
        return word_tokenize(sentence)

    def convert_arr_to_lowercase(self, array):

        for i, value in enumerate(array):
            try:
                lc_value = value.lower()
                array[i] = lc_value
            except Exception as e:
                print("Couldnt convert" + e)
        return array
