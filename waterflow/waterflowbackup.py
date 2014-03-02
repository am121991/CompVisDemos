import Image
import numpy as np
#import scipy.ndimage as ndi
from matplotlib.pyplot import imshow, gray, show
import Queue
from math import exp

import Tkinter, ImageTk

img = Image.open("img1.png").convert('L')
I = np.asarray(img, dtype="int32")
print("size: ", img.size)

W = np.zeros(img.size)

E = np.array(I)
for x in range(img.size[0] - 1):
	for y in range(img.size[1] - 1):
		E[x,y] = abs(2*E[x,y] - E[x+1,y] - E[x,y+1])

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
SPM = 3
lmda = 1
k = 1
alpha = 0.5

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
							acc += W[direction] * cmask[i][x][y]
							if W[direction] == 1:
								muint += I[direction]
								Nint += 1
							else:
								muext += I[direction]
								Next += 1
				FDI = acc/float(SPM)
				VI = FDI / exp(-k * E[element])
				Fp = abs(E[element] - E[target])
				#Fa = E[element[0] + x - 1, element[1] + y - 1]
				Fs = ((-(I[element] - muint)**2*Nint)/(Nint+1)) + (((I[element] - muext)**2*Next)/(Next+1))
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


imshow(W)
gray()
show()

#W[W==1] = 255
#water = Image.fromarray(W, )
#root = Tkinter.Tk()
#tkimage = ImageTk.PhotoImage(water)
#Tkinter.Label(root, image=tkimage).pack()
#root.mainloop()
