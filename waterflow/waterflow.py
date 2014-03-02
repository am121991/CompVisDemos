import Image
import numpy as np
#import scipy.ndimage as ndi
from matplotlib.pyplot import imshow, gray, show
import Queue
from math import exp

import Tkinter, ImageTk

class waterflow(object):
	def __init__(self):
		self.img = Image.open("img1.png").convert('L')
		self.I = np.asarray(self.img, dtype="int32")
		print("size: ", self.img.size)

		self.W = np.zeros(self.img.size)

		self.E = np.array(self.I)
		for x in range(self.img.size[0] - 1):
			for y in range(self.img.size[1] - 1):
				self.E[x,y] = abs(2*self.E[x,y] - self.E[x+1,y] - self.E[x,y+1])

		self.q = Queue.Queue()
		self.empty = False

		# Initialisation
		for x in range(3):
			for y in range(3):
				self.W[249+x, 4+y] = 1
				self.q.put((249+x, 4+y))


		self.cmask = [
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
		self.SPM = 3
		self.lmda = 1
		self.k = 1
		self.alpha = 0.5

		self.root = Tkinter.Tk()
		self.frame = Tkinter.Frame(self.root, width=self.img.size[1], height=self.img.size[0])
		self.frame.pack()
		self.canvas = Tkinter.Canvas(self.frame, width=self.img.size[1], height=self.img.size[0])
		self.canvas.place(x=-2, y=-2)
		self.root.after(0, self.animation)
		self.root.mainloop()

	def animation(self):
		print "start"
		while self.empty == False:
			try: 
				## Contour element processing here
				element = self.q.get(False)
#				print "ce:", element
				for i in range(9):
					if i == 4:
						continue
					target = (element[0] + i/3 - 1, element[1] + i%3 - 1)
#					print "tg:", target
					if target[0] >= 0 and target[0] < self.img.size[0] and target[1] >= 0  and target[1] < self.img.size[1] and self.W[target] == 0:
						acc = 0.0
						muint = 0
						Nint = 0
						muext = 0
						Next = 0
						for x in range(3):
							for y in range(3):
								direction = (element[0] + x - 1, element[1] + y - 1)
								if direction[0] >= 0 and direction[0] < self.img.size[0] and direction[1] >= 0 and direction[1] < self.img.size[1]:
									acc += self.W[direction] * self.cmask[i][x][y]
									if self.W[direction] == 1:
										muint += self.I[direction]
										Nint += 1
									else:
										muext += self.I[direction]
										Next += 1
						FDI = acc/float(self.SPM)
						VI = FDI / exp(-self.k * self.E[element])
						Fp = abs(self.E[element] - self.E[target])
						#Fa = E[element[0] + x - 1, element[1] + y - 1]
						Fs = ((-(self.I[element] - muint)**2*Nint)/(Nint+1)) + (((self.I[element] - muext)**2*Next)/(Next+1))
						F = self.alpha * Fp + (1-self.alpha)*Fs
						#print "V:", VI, " F:", F
						J = F + self.lmda * VI**2
#						print "VI:", VI, "J:", J
						if VI > 0 and J >= 0:
#							print "BY THE WATERS OF MARS!!!"
							self.W[target] = 1
							self.q.put(target)
							water = np.array(self.W)
							water[water==1] = 255
							self.im = Image.fromarray(water)
							self.canvas.create_image(0,0, image=ImageTk.PhotoImage(image=self.im), anchor="nw")
							self.root.update()
				## Put new water elements into queue
			except Queue.Empty:
				empty = True
		print "finish"


#imshow(W)
#gray()
#show()

#W[W==1] = 255
#water = Image.fromarray(W, )
#root = Tkinter.Tk()
#tkimage = ImageTk.PhotoImage(water)
#Tkinter.Label(root, image=tkimage).pack()
#root.mainloop()

waterflow()
