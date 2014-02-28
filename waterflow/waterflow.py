import Image
import numpy as np
import scipy.ndimage as ndi
from matplotlib.pyplot import imshow, gray, show
import Queue

img = Image.open("img1.png").convert('L')
data = np.asarray(img, dtype="int32")
print("size: ", img.size)

W = np.zeros(img.size)

# Initialisation
W[5, 250] = 1 #because why not

q = Queue.Queue()
q.put((5, 250))
empty = False

SPM = 3

while empty == False:
	try: 
		## Contour element processing here
		element = q.get(False)
		print element

		## Put new water elements into queue
	except:
		empty = True


imshow(data)
gray()
show()
