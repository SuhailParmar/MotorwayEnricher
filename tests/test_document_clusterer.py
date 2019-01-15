from lib.document_clusterer import DocumentClusterer


class TestDocumentClusterer:

    dc = DocumentClusterer()
    original_tweet = "m6 congestion traffic j25 southbound south"

    documents = [
        # original_tweet,
        "Lorry Caused The Accident On the m6",
        "M6 incident was caused by overturned lorry",
        "Lorry is flipped over on M6",
        "M6 accident on J25 south",
        "Seems to be an accident on the m6 J25",
    ]

    def test_kmeans_clusterer(self):
        # Key words extracted from original tweet
        # Matrix expects strings, not already parsed arrays
        matrix = self.dc.create_tf_idf_matrix(self.documents)
        v_p_clusters = self.dc.cluster()
        assert len(v_p_clusters) > 0
        assert min(v_p_clusters) == 0
        assert max(v_p_clusters) == 2
        print(v_p_clusters)
        assert False

    """
    def test_create_pandas_dataframe(self):
        matrix = self.dc.create_tf_idf_matrix(self.documents)
        clusters = self.dc.cluster()
        df = self.dc.to_dataframe(self.documents, clusters)
        print(df.head(10))
        assert False
    """
