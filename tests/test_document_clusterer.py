from lib.document_clusterer import DocumentClusterer
from lib.utils import Utils

class TestDocumentClusterer:

    original_tweet = ["m6","congestion","traffic","j25","southbound","south"]

    documents = [
        "Lorry Caused The Accident On the m6 j25",
        "m6 incident was caused by overturned lorry",
        "Lorry is flipped over on m6",
        "m6 accident on j25 south",
        "Seems to be an accident on the m6 j25",
    ]

    def test_cluster(self):
        dc = DocumentClusterer()
        docs = Utils.strip_words(self.documents, self.original_tweet)
        dc.create_tf_idf_matrix(docs)
        x = dc.cluster()


