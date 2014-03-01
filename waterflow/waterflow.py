import Image
import numpy as np
import scipy.ndimage as ndi
from matplotlib.pyplot import imshow, gray, show
import Queue

img = Image.open("img1.png").convert('L')
data = np.asarray(img, dtype="int32")
print("size: ", img.size)

W = np.zeros(img.size)

q = Queue.Queue()
empty = False

# Initialisation
for x in range(3):
	for y in range(3):
		W[249+x, 4+y] = 1
		q.put((249+x, 4+y))


cmask = [
		[
			[-1, -1,  0],
			[-1,  0,  1],
			[ 0,  1,  1]
		],[
			[-1, -1, -1],
			[ 0,  0,  0],
			[ 1,  1,  1]
		],[
			[ 0, -1, -1],
			[ 1,  0, -1],
			[ 1,  1,  0]
		],[
			[ 1,  0, -1],
			[ 1,  0, -1],
			[ 1,  0, -1]
		],[
			[ 1,  1,  0],
			[ 1,  0, -1],
			[ 0, -1, -1]
		],[
			[ 1,  1,  1],
			[ 0,  0,  0],
			[-1, -1, -1]
		],[
			[ 0,  1,  1],
			[-1,  0,  1],
			[-1, -1,  0]
		],[
			[-1,  0,  1],
			[-1,  0,  1],
			[-1,  0 , 1]
		]
	]
SPM = 3
FDI = [0, 0, 0, 0, 0, 0, 0, 0]

while empty == False:
	try: 
		## Contour element processing here
		element = q.get(False)
		print element
		for i in range(8):
			acc = 0.0
			for x in range(3):
				for y in range(3):
					acc += W[element[0] + x - 1, element[1] + y - 1] * cmask[i][x][y]
			FDI[i] = acc/float(SPM)
		print FDI
		## Put new water elements into queue
	except:
		empty = True


imshow(W)
show()
