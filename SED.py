from PIL import Image

print("hello")

img = Image.open("Lenna.png")
img = img.convert('L') # convert to greyscale

pixels = img.load()
print(pixels)

# pixels is an indexable object. Each index is a tuple representing the colour
# edit image using img[x,y] = int

img.show()
