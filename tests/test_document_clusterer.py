from lib.document_clusterer import DocumentClusterer


class TestDocumentClusterer:

    dc = DocumentClusterer()
    original_tweet = "m6 congestion traffic j25 southbound south"

    documents = [
        original_tweet,
        "Lorry Caused The Accident On the m6",
        "M6 incident was caused by overturned lorry",
        "Lorry battered on M6",
        "M6 accident on J25 south",
        "Seems to be an accident on the m6 J25",
    ]

    def test_kmeans_clusterer(self):
        # Key words extracted from original tweet
        # Matrix expects strings, not already parsed arrays
        matrix = self.dc.create_tf_idf_matrix(self.documents)
        clusters = self.dc.kmeans_cluster()
        assert len(clusters) > 0
        assert min(clusters) == 0
        assert max(clusters) == 2

    def test_create_pandas_dataframe(self):
        matrix = self.dc.create_tf_idf_matrix(self.documents)
        clusters = self.dc.kmeans_cluster()
        df = self.dc.to_dataframe(self.documents, clusters)
        df = df.sort_index()
        print(df.head(10))
        assert False