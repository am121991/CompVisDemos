from PIL import Image

img = Image.open("img74.gif")
img = img.convert('L') # convert to greyscale
print("image size:", img.size)

pixels = img.load()

# pixels is an indexable object. Each index is a tuple representing the colour
# edit image using img[x,y] = int

img.show()

# basic edge detection
for x in range(img.size[0] - 1):
	for y in range(img.size[1] - 1):
		pixels[x,y] = 2*pixels[x,y] - pixels[x+1,y] - pixels[x,y+1]

img.show()
