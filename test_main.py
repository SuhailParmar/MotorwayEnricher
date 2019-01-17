from lib.document_clusterer import DocumentClusterer
from lib.document_visualiser import DocumentVisualiser

from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt
import matplotlib as mpl

documents = [
    "Lorry Caused The Accident On the m6 j25",
    "m6 incident was caused by overturned lorry",
    "Lorry is flipped over on m6",
    "m6 accident on j25 south",
    "Seems to be an accident on the m6 j25",
]
original_tweet = "m6 congestion traffic j25 southbound south"

dc = DocumentClusterer()

docs = dc.strip_words(documents, original_tweet.split())
dc.create_tf_idf_matrix(documents)
dc.interpret_matrix()

relevant_values_per_cluster = dc.cluster()
print(relevant_values_per_cluster)

dv = DocumentVisualiser(dc.dist)

#dv.visualiser(dc.cluster_names, dc.tfidf_matrix_terms)

# define the linkage_matrix using ward clustering pre-computed distances
linkage_matrix = ward(dc.dist)

fig, ax = plt.subplots(figsize=(15, 20))  # set size
ax = dendrogram(linkage_matrix, orientation="right",
                labels=["t1", "t2", "t3", "t4", "t5"])

plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout()  # show plot with tight layout

# uncomment below to save figure
plt.savefig('ward_clusters.png', dpi=200)  # save figure as ward_clusters
