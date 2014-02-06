from PIL import Image
import numpy as np
from numpy import pi
import scipy.ndimage as ndi


def non_maximal_edge_suppresion(mag, orient):
    """Non Maximal suppression of gradient magnitude and orientation."""
    # bin orientations into 4 discrete directions
    abin = ((orient + pi) * 4 / pi + 0.5).astype('int') % 4

    mask = np.zeros(mag.shape, dtype='bool')
    mask[1:-1,1:-1] = True
    edge_map = np.zeros(mag.shape, dtype='bool')
    offsets = ((1,0), (1,1), (0,1), (-1,1))
    for a, (di, dj) in zip(range(4), offsets):
        cand_idx = np.nonzero(np.logical_and(abin==a, mask))
        for i,j in zip(*cand_idx):
            if mag[i,j] > mag[i+di,j+dj] and mag[i,j] > mag[i-di,j-dj]:
                edge_map[i,j] = True
    return edge_map


def canny_edges(image, sigma=1.0, low_thresh=50, high_thresh=100):
    """Compute Canny edge detection on an image."""
    image = ndi.filters.gaussian_filter(image, sigma)
    dx = ndi.filters.sobel(image,0)
    dy = ndi.filters.sobel(image,1)

    mag = np.sqrt(dx**2 + dy**2)
    ort = np.arctan2(dy, dx)

    edge_map = non_maximal_edge_suppresion(mag,ort)
    edge_map = np.logical_and(edge_map, mag > low_thresh)

    labels, num_labels = ndi.measurements.label(edge_map, np.ones((3,3)))
    for i in range(num_labels):
        if max(mag[labels==i]) < high_thresh:
            edge_map[labels==i] = False
    return edge_map


#from scipy.misc import lena
from matplotlib.pyplot import imshow, gray, show

img = Image.open("img74.gif").convert('L')
data = np.asarray(img, dtype="int32")

imshow(data)
gray()
show()

data += np.random.normal(0,1,img.size)
imshow(data)
gray()
show()

imshow(canny_edges(data, sigma=0.5))
gray()
show()
