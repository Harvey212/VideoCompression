import numpy as np 
from PIL import Image 
import math

def transToYCbCr(rgb):
	trans=[[0.2126,0.7152,0.0722],[-0.115,-0.386,0.500],[0.500,-0.454,-0.046]]
	temp=np.matmul(trans,np.transpose(rgb))

	y=temp[0]*219+16
	cb=temp[1]*224+128
	cr=temp[2]*224+128

	ycbcrCom=[]
	ycbcrCom.append(int(y))
	ycbcrCom.append(int(cb))
	ycbcrCom.append(int(cr))

	return ycbcrCom

def subSample(imagee):
	img = Image.open(imagee)
	img2=img.convert(mode="RGB")
	r,g,b=img2.split()

	rr=np.array(r)
	gg=np.array(g)
	bb=np.array(b)

	Yma=np.zeros((rr.shape[0],rr.shape[1]),dtype=np.uint8)
	CBma=np.zeros((rr.shape[0],rr.shape[1]),dtype=np.uint8)
	CRma=np.zeros((rr.shape[0],rr.shape[1]),dtype=np.uint8)

	for i in range(rr.shape[0]):
		for j in range(rr.shape[1]):
			rRatio=rr[i][j]/255
			gRatio=gg[i][j]/255
			bRatio=bb[i][j]/255

			com=[]
			com.append(rRatio)
			com.append(gRatio)
			com.append(bRatio)
			resYCBCR=transToYCbCr(com)

			Yma[i][j]=resYCBCR[0]
			CBma[i][j]=resYCBCR[1]
			CRma[i][j]=resYCBCR[2]


	rowturn=int(CBma.shape[0]/2)
	colturn=int(CBma.shape[1]/2)

	CBsampleArray=np.zeros((rowturn,colturn),dtype=np.uint8)
	CRsampleArray=np.zeros((rowturn,colturn),dtype=np.uint8)

	for m in range(rowturn):
		evenrow=2*m
		oddrow=2*m+1
		for n in range(colturn):
			evencol=2*n
			oddcol=2*n+1

			CBleftup=CBma[evenrow][evencol] 
			CBrightup=CBma[evenrow][oddcol]
			CBleftdown=CBma[oddrow][evencol] 
			CBrightdown=CBma[oddrow][oddcol]

			CBsampleArray[m][n]=int((CBleftup/4+CBrightup/4+CBleftdown/4+CBrightdown/4))

			CRleftup=CRma[evenrow][evencol] 
			CRrightup=CRma[evenrow][oddcol]
			CRleftdown=CRma[oddrow][evencol] 
			CRrightdown=CRma[oddrow][oddcol]

			CRsampleArray[m][n]=int((CRleftup/4+CRrightup/4+CRleftdown/4+CRrightdown/4))

	endres=[]
	endres.append(Yma)
	endres.append(CBsampleArray)
	endres.append(CRsampleArray)

	return endres


f1=subSample('foreman_qcif_0_rgb.bmp')
f2=subSample('foreman_qcif_1_rgb.bmp')
f3=subSample('foreman_qcif_2_rgb.bmp')

FF=[f1,f2,f2]

with open("test.yuv", 'w') as fp:
	for pic in FF:
		for chann in pic:
			for i in range(chann.shape[0]):
				for j in range(chann.shape[1]):
					item='{0:08b}'.format(chann[i][j])
					fp.write(item)

			fp.write(' ')

		fp.write('\n')



					
					


		

