from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from lib.natural_language import NaturalLanguage
import pandas as pd


class DocumentClusterer:

    def __init__(self):

        self.nc = NaturalLanguage()

        self.tfidf_vectorizer = TfidfVectorizer(
            min_df=0.1, max_df=0.9, stop_words='english',
            use_idf=True, ngram_range=(1, 3)
        )

        self.tdidf_matrix = None

    def create_tf_idf_matrix(self, documents):
        """
        Create the matrix based on the documents provided
        """
        self.tdidf_matrix = self.tfidf_vectorizer.fit_transform(documents)
        dist = 1 - cosine_similarity(self.tdidf_matrix)  # Required later
        return self.tdidf_matrix

    def cluster(self):
        """
        Based on the original documents provided assign each
        a clustering number.
        """
        # Choose the number of clusters to create
        # Potentially use the GMM model
        n_clusters = 3
        km = KMeans(n_clusters=n_clusters)
        km.fit(self.tdidf_matrix)

        clusters = km.labels_.tolist()
        cluster_centeroids = km.cluster_centers_.argsort()[:, ::-1]

        # All of the vocabulary in the tfidf matrix
        tfidf_matrix_terms = self.tfidf_vectorizer.get_feature_names()

        # Get the indexs of the values closest to the centroid
        # The indexes correlate to the position in the tfidf matrix
        values_closest_to_centroid = 5  # Return the n closest values to that centroid
        relvant_values_per_cluster = {}
        terms = []
        for i in range(0, n_clusters):
            # Get the indexs for each cluster
            tfidf_matrix_indexs = cluster_centeroids[i, :values_closest_to_centroid]
            print("Cluster {}:".format(i))
            for index in tfidf_matrix_indexs:
                term = tfidf_matrix_terms[index]
                print(term)
                terms.append(term)
            print()

            relvant_values_per_cluster[i] = terms

        return relvant_values_per_cluster

    def to_dataframe(self, docs, cluster):
        df = pd.DataFrame(docs, index=cluster, columns=['original_tweet'])
        df.index.rename('cluster', inplace=True)
        return df.sort_index()
