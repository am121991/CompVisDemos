from PIL import Image
from math import *

oimg = Image.open("img74.gif")
# oimg = Image.open("Lenna.png")
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
	return exp(-((r-r0)/float(t))**6)

img2 = oimg.convert('L')
pixels2 = img2.load()

t = 10 								#threshold
r = 3.4 							#mask radius
md = int(ceil(r*2)) #mask dimension
n = [[0 for x in range(img2.size[1])] for x in range(img2.size[0])]	#output
m = [[0 for x in range(md)] for x in range(md)]											#mask
mx = [[0 for x in range(img2.size[1])] for x in range(img2.size[0])]	#output
my = [[0 for x in range(img2.size[1])] for x in range(img2.size[0])]	#output

count = 0							#mask count

for x in range(md):
	for y in range(md):
		if (x-r+0.5)**2 + (y-r+0.5)**2 < r**2:
			m[x][y] = 1
			count += 1
	print m[x]

g = 3*count/4 				#geometric threshold
#g = count/2
print g, count

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		for xr in range(md):
			for yr in range(md):
				xx = x-r+xr
				yy = y-r+yr
				if m[xr][yr] == 1 and xx>=0 and xx<img2.size[0] and yy>=0 and yy<img2.size[1]:
					cdif = c2(pixels2[xx, yy], pixels2[x,y])
					n[x][y] += cdif
					mx[x][y] += cdif*(xr-r)
					my[x][y] += cdif*(yr-r)

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		mx[x][y] /= n[x][y]
		my[x][y] /= n[x][y]

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		if n[x][y] < g:
			n[x][y] = g - n[x][y]
		else:
			n[x][y] = 0

root2 = sqrt(2)
delta = 0.00000000000001

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		if mx[x][y] and my[x][y]:
			ang = atan2(my[x][y], mx[x][y])
			x1 = int(x + ceil((cos(ang+pi/8)*root2)-0.5-delta))
			y1 = int(y + ceil((-sin(ang-pi/8)*root2)-0.5-delta))
			x2 = int(x + ceil((cos(ang-pi/8)*root2)-0.5-delta))
			y2 = int(y + ceil((-sin(ang-pi/8)*root2)-0.5-delta))
			if x1>=0 and x1<img2.size[0] and y1>=0 and y1<img2.size[1] and x2>=0 and x2<img2.size[0] and y2>=0 and y2<img2.size[1]:
				if n[x][y] >= n[x1][y1] and n[x][y] >= n[x2][y2]:
					pixels2[x,y] = n[x][y] * 255/g
				else:
					pixels2[x,y] = 0
		else:
			pixels2[x,y] = n[x][y] * 255/g

img2.show()


