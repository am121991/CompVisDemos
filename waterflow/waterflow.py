import Image
import numpy as np
import scipy.ndimage as ndi
from matplotlib.pyplot import imshow, gray, show

img = Image.open("img1.png").convert('L')
data = np.asarray(img, dtype="int32")

imshow(data)
gray()
show()
