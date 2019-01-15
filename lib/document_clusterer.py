from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from lib.natural_language import NaturalLanguage
import pandas as pd


class DocumentClusterer:

    def __init__(self):

        self.nc = NaturalLanguage()

        self.tdidf_vectorizer = TfidfVectorizer(
            min_df=0.1, max_df=0.9, stop_words='english',
            use_idf=True, ngram_range=(1, 3)
        )

        self.tdidf_matrix = None

    def create_tf_idf_matrix(self, documents):
        """
        Create the matrix based on the documents provided
        """

        self.tdidf_matrix = self.tdidf_vectorizer.fit_transform(documents)

        dist = 1 - cosine_similarity(self.tdidf_matrix)  # Required later
        return self.tdidf_matrix

    def kmeans_cluster(self):
        """
        Based on the original documents provided assign each
        a clustering number.
        """
        clusters = 3
        km = KMeans(n_clusters=clusters)
        km.fit(self.tdidf_matrix)
        clusters = km.labels_.tolist()
        return clusters

    def to_dataframe(self, docs, cluster):
        df = pd.DataFrame(docs, index=cluster, columns=['original_tweet'])
        df.index.rename('cluster', inplace=True)
        return df