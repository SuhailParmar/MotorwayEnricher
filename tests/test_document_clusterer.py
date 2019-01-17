from lib.document_clusterer import DocumentClusterer


class TestDocumentClusterer:

    original_tweet = "m6 congestion traffic j25 southbound south"

    documents = [
        "Lorry Caused The Accident On the m6 j25",
        "m6 incident was caused by overturned lorry",
        "Lorry is flipped over on m6",
        "m6 accident on j25 south",
        "Seems to be an accident on the m6 j25",
    ]

    def test_word_stripper(self):
        dc = DocumentClusterer()
        docs = dc.strip_words(self.documents, self.original_tweet.split())
        assert len(docs) == 5
        assert docs[0] == "Lorry Caused The Accident On the  "

    def test_cluster(self):
        dc = DocumentClusterer()
        docs = dc.strip_words(self.documents, self.original_tweet)
        dc.create_tf_idf_matrix(docs)
        x = dc.cluster()
        assert len(x) == 3
