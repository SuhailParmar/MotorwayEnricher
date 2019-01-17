
import pandas as pd
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt
import matplotlib as mpl


class DocumentVisualiser():

    def __init__(self, distance_matrix):
        # Create a multi-dimensional scaler which takes in
        # a distance matrix
        self.mds = MDS(
            n_components=3, dissimilarity="precomputed", random_state=1)

        self.positions = self.mds.fit_transform(distance_matrix)
        self.x_cords = self.positions[:, 0]
        self.y_cords = self.positions[:, 1]
        print(self.x_cords)
        print(self.y_cords)

    def visualiser(self, distance_matrix):
        # define the linkage_matrix using ward clustering pre-computed distances
        linkage_matrix = ward(distance_matrix)

        fig, ax = plt.subplots(figsize=(15, 20))  # set size
        ax = dendrogram(linkage_matrix, orientation="right",
                        labels=["t1", "t2", "t3", "t4", "t5"])# TODO make dynamic

        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off')

        plt.tight_layout()  # show plot with tight layout

        # uncomment below to save figure
        plt.savefig('ward_clusters.png', dpi=200)  # save figure as ward_clusters

        pass
