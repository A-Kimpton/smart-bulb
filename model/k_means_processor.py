import cv2
from sklearn.cluster import MiniBatchKMeans, KMeans
import numpy as np
import time

class DominantColors:

    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None

    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image

    def dominantColors(self):

        #read image

        img = np.array(self.IMAGE)
        #reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))

        #save image after operations
        self.IMAGE = img

        #using k-means to cluster pixels
        kmeans = KMeans(n_clusters = self.CLUSTERS)
        #kmeans = MiniBatchKMeans(n_clusters = self.CLUSTERS)

        # fir the points to kmeans algo
        kmeans.fit(img)

        #the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_

        #save labels
        self.LABELS = kmeans.labels_



        #returning after converting to integer from float
        return self.COLORS.astype(int)
