from lib.natural_language import NaturalLanguage


class TestNaturalLanguage:

    nl = NaturalLanguage()

    def test_lower_case_convertion(self):
        response = self.nl.tokenize("Hello, my name is Suhail")
        assert response == ["Hello", ",", "my", "name", "is", "Suhail"]

    def test_convert_to_lower_case(self):
        response = self.nl.convert_to_lowercase(
            ["J25", ",", "my", "name", "is", "Suhail"])
        assert response == ["j25", ",", "my", "name", "is", "suhail"]
