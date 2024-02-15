import numpy as np 
from PIL import Image 

############################################
img = Image.open('foreman_qcif_0_rgb.bmp')   #previous
img2= Image.open('foreman_qcif_1_rgb.bmp')   #after

y,cb,cr=img.convert('YCbCr').split()
yy,cbb,crr=img2.convert('YCbCr').split()

y1=np.array(y) #previous
y2=np.array(yy)#after
##############################################
#decide how many blocks to do
blockrows=int(y2.shape[0]/16)  #if there are 32 rows, ans is 2. you will loop 0,1 as origin
blockcolumns=int(y2.shape[1]/16)
###########################################
collage=np.zeros((y1.shape[0],y1.shape[1]))
#######################################
finalansX=[]
finalansY=[]

for i in range(blockrows):
	#you won't get to the blockrows-th
	blockrowori=16*i #the actual row-th

	searchup=blockrowori-16   #the actual rowth
	searchdown=blockrowori+16 #the actual rowth+1

	if searchup<0:
		searchup=0

	if searchdown>=y1.shape[0]:
		searchdown=y1.shape[0]  #the limit of actual rowth+1

	for j in range(blockcolumns):  #you won't get to the limit
		blockcolumnori=16*j #the actual column th

		#####################
		searchleft=blockcolumnori-16
		searchright=blockcolumnori+16 #the actual column+1 

		if searchleft<0:
			searchleft=0		

		if searchright>=y1.shape[1]:
			searchright=y1.shape[1] #the actual limit of column-th limit+1

		##############################
		#to create the block pixels in the after block
		#you have to recreate new compare block when you move to new block
		s1=0
		compareArr=np.zeros((16,16))
		for c1 in range(blockrowori,(blockrowori+16)):
			s2=0
			for c2 in range(blockcolumnori,(blockcolumnori+16)):
				compareArr[s1][s2]=y2[c1][c2] #y2 is the after image
				s2+=1
			s1+=1
		####################
		#to find the most similar counterpart
		corxs=[]
		corys=[]

		sads=[]

		#(m,n) represent the leftup corner
		for m in range(searchup,searchdown):
			for n in range(searchleft,searchright):
				LL=n
				RR=n+15 #the actual column
				UU=m
				DD=m+15 #the actual row

				sad=0

				if (DD>=y1.shape[0]) or (RR>=y1.shape[1]):
					pass
				else:
					corxs.append(n)
					corys.append(m)
					
					s1=0
					for vv in range(UU,(DD+1)):
						s2=0
						for hh in range(LL,(RR+1)):
							sad+=abs(y1[vv][hh]-compareArr[s1][s2])
							s2+=1
						s1+=1

					sads.append(sad)

		ind = np.argmin(sads)
		xx=corxs[ind]
		yy=corys[ind]
		
		mvy=blockrowori-yy
		mvx=blockcolumnori-xx

		finalansX.append(mvx)
		finalansY.append(mvy)


		s1=0
		for w1 in range(blockrowori,(blockrowori+16)):
			s2=0
			g1=yy+s1
			for w2 in range(blockcolumnori,(blockcolumnori+16)):
				g2=xx+s2
				collage[w1][w2]=y1[g1][g2]
				s2+=1
			s1+=1

blockth=0

for i in range(blockrows):
	for j in range(blockcolumns):
		ans="Block "+str(blockth)+"-("+str(finalansX[blockth])+","+str(finalansY[blockth])+")"
		print(ans)
		blockth+=1


#,dtype=np.uint8
#############################################################
ress=Image.fromarray(collage)
ress.show()
ress = ress.convert('RGB')
ress.save("1b.jpg")