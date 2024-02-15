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

def transToRGB(ycb):
	TRANS=np.array([[0.2126,0.7152,0.0722],[-0.115,-0.386,0.500],[0.500,-0.454,-0.046]])
	sR=(ycb[0]-16)/219
	sG=(ycb[1]-128)/224
	sB=(ycb[2]-128)/224

	com1=[]
	com1.append(sR)
	com1.append(sG)
	com1.append(sB)

	RES=np.matmul(np.linalg.inv(TRANS),np.transpose(com1))

	return RES



##################################################3
img = Image.open('foreman_qcif_0_rgb.bmp')
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

########################################
res1=Image.fromarray(Yma)
res2=Image.fromarray(CBma)
res3=Image.fromarray(CRma)

res1.show()
res2.show()
res3.show()

rowturn=int(CBma.shape[0]/2)
colturn=int(CBma.shape[1]/2)

rowodd=CBma.shape[0]%2
colodd=CBma.shape[1]%2

##################################

CBsampleArray=np.zeros((CBma.shape[0],CBma.shape[1]),dtype=np.uint8)
CRsampleArray=np.zeros((CRma.shape[0],CRma.shape[1]),dtype=np.uint8)

for m in range(rowturn):
	evenrow=2*m
	oddrow=2*m+1
	for n in range(colturn):
		evencol=2*n
		oddcol=2*n+1

		#############################################
		CBleftup=CBma[evenrow][evencol] 
		CBrightup=CBma[evenrow][oddcol]
		CBleftdown=CBma[oddrow][evencol] 
		CBrightdown=CBma[oddrow][oddcol]

		CBavg=int((CBleftup/4+CBrightup/4+CBleftdown/4+CBrightdown/4))
		CBsampleArray[evenrow][evencol]=CBavg 
		CBsampleArray[evenrow][oddcol]=CBavg
		CBsampleArray[oddrow][evencol]=CBavg 
		CBsampleArray[oddrow][oddcol]=CBavg
		##############################################

		CRleftup=CRma[evenrow][evencol] 
		CRrightup=CRma[evenrow][oddcol]
		CRleftdown=CRma[oddrow][evencol] 
		CRrightdown=CRma[oddrow][oddcol]

		CRavg=int((CRleftup/4+CRrightup/4+CRleftdown/4+CRrightdown/4))
		CRsampleArray[evenrow][evencol]=CRavg 
		CRsampleArray[evenrow][oddcol]=CRavg
		CRsampleArray[oddrow][evencol]=CRavg 
		CRsampleArray[oddrow][oddcol]=CRavg

##################################################
if colodd==1:
	for i in range(rowturn):
		evenrow=2*i
		oddrow=2*i+1

		finalcol=CBma.shape[1]-1

		CBup=CBma[evenrow][finalcol]
		CBdown=CBma[oddrow][finalcol]

		CB2avg=int((CBup/2+CBdown/2))
		CBsampleArray[evenrow][finalcol]=CB2avg 
		CBsampleArray[oddrow][finalcol]=CB2avg
		#######################################

		CRup=CRma[evenrow][finalcol]
		CRdown=CRma[oddrow][finalcol]

		CR2avg=int((CRup/2+CRdown/2))
		CRsampleArray[evenrow][finalcol]=CR2avg 
		CRsampleArray[oddrow][finalcol]=CR2avg

####################################################
if rowodd==1:
	for j in range(colturn):
		evencol=2*j
		oddcol=2*j+1

		finalrow=CBma.shape[0]-1

		CBleft=CBma[finalrow][evencol]
		CBright=CBma[finalrow][oddcol]

		CB2avg=int((CBleft/2+CBright/2))
		CBsampleArray[finalrow][evencol]=CB2avg 
		CBsampleArray[finalrow][oddcol]=CB2avg
		#######################################

		CRleft=CRma[finalrow][evencol]
		CRright=CRma[finalrow][oddcol]

		CR2avg=int((CRleft/2+CRright/2))
		CRsampleArray[finalrow][evencol]=CR2avg 
		CRsampleArray[finalrow][oddcol]=CR2avg

if (rowodd==1) and (colodd==1):
	finalrow=CBma.shape[0]-1
	finalcol=CBma.shape[1]-1

	CBsampleArray[finalrow][finalcol]=CBma[finalrow][finalcol]
	CRsampleArray[finalrow][finalcol]=CRma[finalrow][finalcol]

afterR=np.zeros((rr.shape[0],rr.shape[1]),dtype=np.uint8)
afterG=np.zeros((rr.shape[0],rr.shape[1]),dtype=np.uint8)
afterB=np.zeros((rr.shape[0],rr.shape[1]),dtype=np.uint8)

for i in range(afterR.shape[0]):
	for j in range(afterR.shape[1]):
		yy=Yma[i][j]
		cbb=CBsampleArray[i][j]
		crr=CRsampleArray[i][j]

		com=[]
		com.append(yy)
		com.append(cbb)
		com.append(crr)
		res=transToRGB(com)

		r1=res[0]*255
		g1=res[1]*255
		b1=res[2]*255

		afterR[i][j]=r1
		afterG[i][j]=g1
		afterB[i][j]=b1


fr=Image.fromarray(afterR)
fg=Image.fromarray(afterG)
fb=Image.fromarray(afterB)

ress=Image.merge(mode='RGB',bands=(fr,fg,fb))

ress.show()

summ=0
summ2=0
summ3=0

for i in range(afterR.shape[0]):
	for j in range(afterR.shape[1]):
		summ+=(float(afterR[i][j])-float(rr[i][j]))**2
		summ2+=(float(afterG[i][j])-float(gg[i][j]))**2
		summ3+=(float(afterB[i][j])-float(bb[i][j]))**2

mse=summ/(afterR.shape[0]*afterR.shape[1])
mse2=summ2/(afterG.shape[0]*afterG.shape[1])
mse3=summ3/(afterB.shape[0]*afterB.shape[1])

psnr=10*math.log10(255/mse)
psnr2=10*math.log10(255/mse2)
psnr3=10*math.log10(255/mse3)

print("PSNR for red channel: "+str(psnr))
print("PSNR for green channel: "+str(psnr2))
print("PSNR for blue channel: "+str(psnr3))
