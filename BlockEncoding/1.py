import numpy as np 
from PIL import Image
import math
import cmath

import cv2 as cv
from matplotlib import pyplot as plt


img = Image.open('foreman_qcif_0_rgb.bmp')  
y,cb,cr=img.convert('YCbCr').split()
y1=np.array(y)

M=y1.shape[0]
N=y1.shape[1]

def myfunction():
	FF=np.zeros((M,N))

	count=0

	for u in range(M):
		for v in range(N):
			summ=0
		
			for x in range(M):
				for y in range(N):
					summ+=y1[x][y]*cmath.exp(complex(0,-1)*(2*math.pi)*( ((u*x)/M) + ((v*y)/N) ))*pow(-1,(x-y))

			FF[u][v]=np.log(np.abs(summ/(M*N))+1)
			print(count)
			count+=1


	final=(FF/FF.max())*255

	ress=Image.fromarray(final)
	ress.show()

def usebuiltin():
	f = np.fft.fft2(y1)
	fshift = np.fft.fftshift(f)
	magnitude_spectrum = 20*np.log(np.abs(fshift))
	plt.subplot(121),plt.imshow(img, cmap = 'gray')
	plt.title('Input Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
	plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
	plt.show()


#myfunction()
usebuiltin()

