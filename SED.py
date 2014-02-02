from PIL import Image

oimg = Image.open("img74.gif")
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

img2 = oimg.convert('L')
pixels2 = img2.load()

t = 5
n = [[0 for x in range(img2.size[1])] for x in range(img2.size[0])]
g = 3*9/4

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		for xx in range(x-1, x+2):
			for yy in range(y-1, y+2):
				if xx>=0 and xx<img2.size[0] and yy>=0 and yy<img2.size[1]:
					n[x][y] += c(pixels[xx, yy], pixels[x,y])

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		if n[x][y] < g:
			n[x][y] = g - n[x][y]
		else:
			n[x][y] = 0

for x in range(img2.size[0]):
	for y in range(img2.size[1]):
		pixels2[x,y] = n[x][y] * 255

img2.show()
