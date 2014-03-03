import Image
import numpy as np
#import scipy.ndimage as ndi
from matplotlib.pyplot import imshow, gray, show, savefig
import Queue
from math import exp, sqrt
from scipy import ndimage
import os
import datetime

SAVE = False # saving / animating images
CAPTURE = 400 # number of frames to iterate before displaying

if SAVE:
	path = os.path.join( os.path.dirname(__file__), 'recordings', datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
	print path
	os.makedirs(path)

img = Image.open("img4.png").convert('L')
I = np.asarray(img, dtype="int32")
print("size: ", img.size)
imshow(I)
show()

W = np.zeros((img.size[1], img.size[0]))
imshow(W)
show()

Ex = ndimage.sobel(I, 0)  # horizontal derivative
Ey = ndimage.sobel(I, 1)  # vertical derivative
E = np.hypot(Ex, Ey)  # magnitude
E *= 255.0 / np.max(E)
print np.max(E)
imshow(Ex)
show()
imshow(Ey)
show()
imshow(E)
show()

q = Queue.Queue()
empty = False

# Initialisation
for x in range(3):
	for y in range(3):
		W[91+x, 1+y] = 1
		q.put((91+x, 1+y))


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
			[ -1,  0, 1],
			[ -1,  0, 1],
			[ -1,  0, 1]
		],[],[
			[ 1,  0, -1],
			[ 1,  0, -1],
			[ 1,  0, -1]
		],[
			[ 0,  1,  1],
			[-1,  0,  1],
			[-1, -1,  0]
		],[
			[ 1,  1,  1],
			[ 0,  0,  0],
			[-1, -1, -1]
		],[
			[ 1,  1,  0],
			[ 1,  0, -1],
			[ 0, -1, -1]
		]
	]

t = 1
SPM = 3+t*2
lmda = 1
k = 5
alpha = 0.5

def contour(direction):
	for m in range(3):
		for n in range(3):
			x = direction[0]+m-1
			y = direction[1]+n-1
			if x >= 0 and x < img.size[0] and y >= 0 and y < img.size[1] and W[x, y] == 0:
				return -t
	return 1

iteration = 0

while empty == False:
	try: 
		## Contour element processing here
		element = q.get(False)
#		print "ce:", element
		for i in range(9):
			if i == 4:
				continue
			target = (element[0] + i/3 - 1, element[1] + i%3 - 1)
#			print "tg:", target
			if target[0] >= 0 and target[0] < img.size[0] and target[1] >= 0  and target[1] < img.size[1] and W[target] == 0:
				acc = 0.0
				muint = 0
				Nint = 0
				muext = 0
				Next = 0
				for x in range(3):
					for y in range(3):
						direction = (element[0] + x - 1, element[1] + y - 1)
						if direction[0] >= 0 and direction[0] < img.size[0] and direction[1] >= 0 and direction[1] < img.size[1]:
							acc += W[direction] * cmask[i][x][y] * contour(direction)
							if W[direction] == 1:
								muint += I[direction]
								Nint += 1
							else:
								muext += I[direction]
								Next += 1
				FDI = acc/float(SPM)
				VI = FDI / (exp(-k * E[element])+0.00000000000000001)  #check E
				Fp = abs(E[element] - E[target]) #check gradient difference
				#Fa = E[element[0] + x - 1, element[1] + y - 1]
				Fs = - (((I[element] - muint)**2*Nint)/(Nint+1)) + (((I[element] - muext)**2*Next)/(Next+1))
				F = alpha * Fp + (1-alpha)*Fs
				#print "V:", VI, " F:", F
				J = F + lmda * VI**2
#				print "VI:", VI, "J:", J
				if VI > 0 and J >= 0:
#					print "BY THE WATERS OF MARS!!!"
					W[target] = 1;
					q.put(target)
		## Put new water elements into queue
	except Queue.Empty:
		empty = True

	if iteration%CAPTURE == 0:
		imshow(W)
		gray()

		if SAVE:
			image = os.path.join(path, 'frame'+str(iteration).zfill(6)+'.png')
			print 'saving ' + image + ' ...'
			savefig(image)
		else:
			show()

	iteration += 1

if SAVE:
	print 'converting ' + path + ' ...'
	os.system('convert -quality 80 ' + path + '/*.png animation.gif')
	print 'done!'