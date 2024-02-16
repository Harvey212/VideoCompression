import numpy as np
import cv2

def show(imm,nam):
	cv2.imshow(nam,imm/255)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

############################################
#basic setting
M =np.array([[0.299,0.587,0.114],[-0.169,-0.331,0.500],[0.500,-0.419,-0.081]])

img = cv2.imread('original.png')
b,g,r=cv2.split(img)

rows=b.shape[0]
col=b.shape[1]


###############################################3
#conversion of rgb to ycbcr
Y=np.zeros((rows,col), dtype = float)#np.zeros((rows,col), dtype = float)#dtype=np.uint8
cb=np.zeros((rows,col), dtype = float)
cr=np.zeros((rows,col), dtype = float)

for i in range(rows):
	for j in range(col):
		bp=b[i,j]
		gp=g[i,j]
		rp=r[i,j]

		temp=np.array([rp,gp,bp]).transpose()
		res=np.matmul(M,temp)
		Y[i,j]=res[0]#(0.299*rp+0.587*gp+0.114*bp)#res[0]
		cb[i,j]=res[1]#(-0.169*rp-0.331*gp+0.5*bp)#res[1]
		cr[i,j]=res[2]#(0.5*rp-0.419*gp-0.081*bp)#res[2]

show(Y,'y channel')
############################################
#implement 4:2:0 compression
hr=int(rows/2)
if (rows%2)!=0:
	hr+=1

hc=int(col/2)
if (col%2)!=0:
	hc+=1

CB=np.zeros((hr,hc), dtype = float)
CR=np.zeros((hr,hc), dtype = float)


#for m in range(0,7,2):
#	print(m)


ridx=0
cidx=0

for i in range(0,rows,2):
	cidx=0
	for j in range(0,col,2):
		p1=0
		p2=0
		p3=0
		p4=0

		p1p=0
		p2p=0
		p3p=0
		p4p=0

		con1=False
		con2=False

		if (i+1)<rows:
			con1=True
		if (j+1)<col:
			con2=True

		p1 = cb[i,j]
		p1p= cr[i,j]

		if con2:
			p2=cb[i,j+1]
			p2p=cr[i,j+1]
		else:
			p2=cb[i,j]
			p2p=cr[i,j]

		if con1:
			p3=cb[i+1,j]
			p3p=cr[i+1,j]
		else:
			p3=cb[i,j]
			p3p=cr[i,j]

		if con1 and con2:
			p4=cb[i+1,j+1]
			p4p=cr[i+1,j+1]
		else:
			if not con1:
				p4=p2
				p4p=p2p
			else:
				p4=p3
				p4p=p3p	


		CB[ridx,cidx]=(p1+p2+p3+p4)/4
		CR[ridx,cidx]=(p1p+p2p+p3p+p4p)/4
		
		cidx+=1

	ridx+=1

cv2.imwrite('cb.png',CB)
cv2.imwrite('cr.png',CB)
#####################################
#reconstruction
rCB=np.zeros((rows,col), dtype = float)
rCR=np.zeros((rows,col), dtype = float)

row1=0
row2=0
col1=0
col2=0
#################3

for i in range(rCB.shape[0]):
	##################
	if i%2==0:
		row1=int(i/2)
		row2=int(i/2)
	else:
		row1=int((i-1)/2)
		if (i+1)<rCB.shape[0]:
			row2=int((i+1)/2)
		else:
			row2=row1
	###########################
	for j in range(rCB.shape[1]):

		if j%2==0:
			col1=int(j/2)
			col2=int(j/2)
		else:
			col1=int((j-1)/2)
			if (j+1)<rCB.shape[1]:
				col2=int((j+1)/2)
			else:
				col2=col1
			
		##
		rCR[i,j]=(CR[row1,col1]+CR[row1,col2]+CR[row2,col1]+CR[row2,col2])/4
		rCB[i,j]=(CB[row1,col1]+CB[row1,col2]+CB[row2,col1]+CB[row2,col2])/4

#####################################
#convert from ycbcr to rgb		
R=np.zeros((rows,col), dtype = float)
G=np.zeros((rows,col), dtype = float)
B=np.zeros((rows,col), dtype = float)

Minv=np.linalg.inv(M)

for i in range(rows):
	for j in range(col):

#		yp=Y[i,j]
#		cbp=cb[i,j]
#		crp=cr[i,j]


		temp=np.array([Y[i,j],cb[i,j],cr[i,j]]).transpose()#rCB[i,j],rCR[i,j]
		res=np.matmul(Minv,temp)
		R[i,j]=res[0]#(yp*1+cbp*0+1.402*crp)#res[0]
		G[i,j]=res[1]#(yp*1-0.344*cbp-0.714*crp)#res[1]
		B[i,j]=res[2]#(yp*1+1.772*cbp+crp*0)#res[2]


image_merge = cv2.merge([B, G, R])
show(image_merge,'reconstruction')

cv2.imwrite('reconstruction.png',image_merge)




