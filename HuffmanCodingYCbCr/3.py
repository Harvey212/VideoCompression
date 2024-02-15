import numpy as np 
from PIL import Image 
import math


def stat(arr):
	batch1Count=0
	batch2Count=0
	batch3Count=0
	batch4Count=0
	batch5Count=0
	totalpixel=arr.shape[0]*arr.shape[1]

	for i in range(arr.shape[0]):
		for j in range(arr.shape[1]):
			if arr[i][j]<=51:
				batch1Count+=1
			if (arr[i][j]>51) and (arr[i][j]<=102):
				batch2Count+=1
			if (arr[i][j]>102) and (arr[i][j]<=153):
				batch3Count+=1
			if (arr[i][j]>153) and (arr[i][j]<=204):
				batch4Count+=1
			if (arr[i][j]>204) and (arr[i][j]<=255):
				batch5Count+=1
	batch1prob=batch1Count/totalpixel
	batch2prob=batch2Count/totalpixel
	batch3prob=batch3Count/totalpixel
	batch4prob=batch4Count/totalpixel
	batch5prob=batch5Count/totalpixel

	namee="block     probability"
	#print(namee)
	#print("block0    "+str(batch1prob))
	#print("block1    "+str(batch2prob))
	#print("block2    "+str(batch3prob))
	#print("block3    "+str(batch4prob))
	#print("block4    "+str(batch5prob))

	#
	#test=[batch1prob,batch2prob,batch3prob,batch4prob,batch5prob]
	#print(test)
	#

	wait={'1':batch1prob,'2':batch2prob,'3':batch3prob,'4':batch4prob,'5':batch5prob}
	sortwait={k: v for k, v in sorted(wait.items(), key=lambda item: item[1])}

	encodename=[]
	for _ in range(len(wait.keys())):
		encodename.append([])         #reverse

	while len(sortwait)>1:
		temp=list(sortwait)
		smallest=temp[0]
		secondsmall=temp[1]



		for m in range(len(smallest)):
			encodename[int(smallest[m])-1].append(0)

		for n in range(len(secondsmall)):
			encodename[int(secondsmall[n])-1].append(1)

		comwho=smallest+secondsmall
		comprob=sortwait[smallest]+sortwait[secondsmall]
		wait.pop(smallest)
		wait.pop(secondsmall)

		wait[comwho]=comprob
		sortwait={k: v for k, v in sorted(wait.items(), key=lambda item: item[1])}

	finalans=[]
	for u in range(len(encodename)):
		tarr=encodename[u]
		last=len(tarr)-1
		ans=''
		for k in range(last,-1,-1):
			ans+=str(tarr[k])

		finalans.append(ans)

	search={}

	for index in range(len(finalans)):
		name="block"+str(index)
		search[name]=finalans[index]

	return search


def cal(imagee):
	img = Image.open(imagee)
	img2=img.convert(mode="RGB")
	r,g,b=img2.split()

	rr=np.array(r)
	gg=np.array(g)
	bb=np.array(b)

	color=["red","green","blue"]
	colorarr=[rr,gg,bb]

	#title="encoding result for "+imagee+":"
	#print(title)
	for g in range(len(color)):
		sub=color[g]+" channel:"
	#	print(sub)
		test=stat(colorarr[g])
	
	#print('\n')	


def total(ima):
	img = Image.open(ima)
	img2=img.convert(mode="RGB")
	R,G,B=img2.split()

	f1=bitstreamtest(R)
	f2=bitstreamtest(G)
	f3=bitstreamtest(B)

	rows=np.array(R).shape[0]
	col=np.array(R).shape[1]

	rgbArray = np.zeros((rows,col,3), 'uint8')
	rgbArray[..., 0] = f1
	rgbArray[..., 1] = f2
	rgbArray[..., 2] = f3
	ikk = Image.fromarray(rgbArray)

	ikk.show()




	#k1 = Image.fromarray(f1,mode='RGB')
	#k2 = Image.fromarray(f2,mode='RGB')
	#k3 = Image.fromarray(f3,mode='RGB')

	#im1 = Image.merge(mode='RGB',bands=(k1, k2, k3))
	#im1.show()


def bitstreamtest(r):
	

	#print("test for bitstream of red channel:")

	rr=np.array(r)


	rows=rr.shape[0]
	col=rr.shape[1]



	se=stat(rr)


	test={}

	for k,v in se.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
		test[v]=k	

	finalbitstream=''

	for i in range(rr.shape[0]):
		for j in range(rr.shape[1]):
			bitstreamm=0
			if rr[i][j]<=51:
				bitstreamm=se['block0']
			if (rr[i][j]>51) and (rr[i][j]<=102):
				bitstreamm=se['block1']
			if (rr[i][j]>102) and (rr[i][j]<=153):
				bitstreamm=se['block2']
			if (rr[i][j]>153) and (rr[i][j]<=204):
				bitstreamm=se['block3']
			if (rr[i][j]>204) and (rr[i][j]<=255):
				bitstreamm=se['block4']

			finalbitstream+=bitstreamm



			#print(bitstreamm, end='')
	#print(finalbitstream)
	result=''

	imm=[]

	for k in finalbitstream:
		result+=k

		if result in list(test.keys()):
			blo=test[result]

			if blo=='block0':
				imm.append(51)
			if blo=='block1':
				imm.append(102)
			if blo=='block2':
				imm.append(153)
			if blo=='block3':
				imm.append(204)
			if blo=='block4':
				imm.append(255)

			result=''

	ff=np.zeros((rows,col))
	count=0
	for i in range(rows):
		for j in range(col):
			ff[i][j]=imm[count]
			count+=1

	
	return ff


	#if '101' in list(se.values()):
	#	print('yes')

	
#def decodebit(bitt)



#cal('foreman_qcif_0_rgb.bmp')
#cal('foreman_qcif_1_rgb.bmp')
#cal('foreman_qcif_2_rgb.bmp')

total('foreman_qcif_0_rgb.bmp')

