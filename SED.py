from PIL import Image
from math import *
from numpy import random

oimg = Image.open("lenna.png")
img = oimg.convert('L') # convert to greyscale
print("image size:", img.size)

pixels = img.load()

# pixels is an indexable object. Each index is a tuple representing the colour
# edit image using img[x,y] = int

img.show()

# basic edge detection
for x in range(img.size[0] - 1):
	for y in range(img.size[1] - 1):
		pixels[x,y] = abs(2*pixels[x,y] - pixels[x+1,y] - pixels[x,y+1])

img.show()

# Susan edge detection with 3x3 mask

def c(r, r0):
	global t
	if (abs(r - r0) > t):
		return 0
	else:
		return 1

def c2(r, r0):
	global t
	return exp(-((r-r0)/t)**6)

img2 = oimg.convert('L')
pixels2 = img2.load()

#for x in range(img2.size[0]):	#add noise
#	for y in range(img2.size[1]):
#		pixels2[x,y] += random.normal(0,5)
#img2.show()


t = 10 								#threshold
r = 3.4 							#mask radius
md = int(ceil(r*2)) #mask dimension
n = [[0.0 for x in range(img2.size[1])] for x in range(img2.size[0])]	#output
m = [[0.0 for x in range(md)] for x in range(md)]											#mask
count = 0							#mask count

for x in range(md):
	for y in range(md):
		if (x-r+0.5)**2 + (y-r+0.5)**2 < r**2:
			m[x][y] = 1
			count += 1
	print m[x]

g = 3.0*count/4.0 				#geometric threshold
print g, count

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		for xr in range(md):
			for yr in range(md):
				xx = x-r+xr
				yy = y-r+yr
				if m[xr][yr] == 1 and xx>=0 and xx<img2.size[0] and yy>=0 and yy<img2.size[1]:
					n[x][y] += c2(pixels2[xx, yy], pixels2[x,y])

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		if n[x][y] < g:
			n[x][y] = g - n[x][y]
		else:
			n[x][y] = 0

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		pixels2[x,y] = n[x][y] * 255/g

img2.show()

