from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from lib.natural_language import NaturalLanguage
import pandas as pd
import numpy as np
import logging

dc_logger = logging.getLogger("DocumentClusterer")


class DocumentClusterer:

    def __init__(self):

        self.nc = NaturalLanguage()

        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            use_idf=True,
            min_df=0.1,
            max_df=0.9,
            # min_df=0.1, max_df=0.9, stop_words='english',
            # use_idf=True, ngram_range=(1, 3)
        )

        self.tdidf_matrix = None
        self.weights_df = None
        self.dist = None
        self.cluster_names = None
        self.tfidf_matrix_terms = None

    def create_tf_idf_matrix(self, documents):
        """
        Create a TF*IDF matrix based on the documents provided
        """
        self.tdidf_matrix = self.tfidf_vectorizer.fit_transform(documents)
        self.dist = 1 - cosine_similarity(self.tdidf_matrix)
        return self.tdidf_matrix

    def create_term_weight_df(self):
        terms = self.tfidf_vectorizer.get_feature_names()
        weights = np.asarray((self.tdidf_matrix.mean(axis=0))).ravel().tolist()
        weights_df = pd.DataFrame({'term': terms, 'weight': weights})
        self.weights_df = weights_df.sort_values(by='weight', ascending=False)
        dc_logger.debug(weights_df.head(20))

    def cluster(self, n_clusters=2):
        # Based on the original documents provided assign each
        # a clustering number.
        # Choose the number of clusters to create
        # Potentially use the GMM model
        km = KMeans(n_clusters=n_clusters)
        km.fit(self.tdidf_matrix)

        self.cluster_names = km.labels_.tolist()
        cluster_centeroids = km.cluster_centers_.argsort()[:, ::-1]

        # All of the vocabulary in the tfidf matrix
        self.tfidf_matrix_terms = self.tfidf_vectorizer.get_feature_names()
        # Get the indexs of the values closest to the centroid
        # The indexes correlate to the position in the tfidf matrix
        values_closest_to_centroid = 5  # Return the n closest values to that centroid
        relvant_values_per_cluster = {}
        for i in range(0, n_clusters):
            terms = []

            # Get the indexs for each cluster
            tfidf_matrix_indexs = cluster_centeroids[i,
                                                     :values_closest_to_centroid]
            dc_logger.info("Cluster {}:".format(i))
            print("Cluster {}:".format(i))
            for index in tfidf_matrix_indexs:
                term = self.tfidf_matrix_terms[index]
                dc_logger.info(term)
                print(term)
                terms.append(term)
            dc_logger.info('---')

            relvant_values_per_cluster[i] = terms

        return relvant_values_per_cluster

    def to_dataframe(self, docs, cluster):
        df = pd.DataFrame(docs, index=cluster, columns=['original_tweet'])
        df.index.rename('cluster', inplace=True)
        return df.sort_index()

    def main(self, documents):
        self.create_tf_idf_matrix(documents)
        self.create_term_weight_df()
        v_p_clusters = self.cluster()
        # dc_logger.info(v_p_clusters)
