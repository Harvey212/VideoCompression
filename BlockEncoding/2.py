import numpy as np 
from PIL import Image
import math
import cmath
import cv2

def printzigzag(matrix):
	
	#rows=len(matrix)
	#columns=len(matrix[0])

	rows=matrix.shape[0]
	columns=matrix.shape[1]

	#index=np.zeros((rows,columns))
	#count=0
	#for i in range(rows):
	#	for j in range(columns):
	#		index[i][j]=int(count) 
	#		count+=1

	solution=[[] for i in range(rows+columns-1)]
	#indexsolution=[[] for i in range(rows+columns-1)]

	for i in range(rows):
		#temp=matrix[i]
		for j in range(columns):
			summ=i+j
			if summ%2==0:
				solution[summ].insert(0,matrix[i][j])
				#solution[summ].insert(0,temp[j])
				#indexsolution[summ].insert(0,index[i][j])
			else:
				solution[summ].append(matrix[i][j])
				#solution[summ].append(temp[j])
				#indexsolution[summ].append(index[i][j])

	ans=[]
	for i in solution:
		for j in i:
			ans.append(j)

	return ans
	#for i in range(len(solution)):
	#	subs=solution[i]
	#	subindex=indexsolution[i]
	#	for j in range(len(subs)):

	#		name="Block: "+str(int(subindex[j]))
	#		print(name)

	#		ans=[]
	#		tar=np.array(subs[j])
	#		for m in range(tar.shape[0]):
	#			for n in range(tar.shape[1]):
	#				ans.append(tar[m][n])
	#		print(ans)
	
##################################################

img = Image.open('foreman_qcif_0_rgb.bmp')  
y,cb,cr=img.convert('YCbCr').split()
y1=np.array(y)

M=int(y1.shape[0]/8) 
N=int(y1.shape[1]/8)

#fakematrix=[]

#fakecount=0
count=0

for startrow in range(M):
	endrow=startrow+8

	#fakematrix.append([])
	for startcol in range(N):
		endcol=startcol+8

		temp=np.zeros((8,8))
		s1=0
		s2=0
		for i in range(startrow,endrow):
			s2=0
			for j in range(startcol,endcol):
				temp[s1][s2]=y1[i][j]
				s2+=1
			s1+=1

		dct = cv2.dct(temp)
		res=printzigzag(dct)
		name="Block: "+str(int(count))
		print(name)
		count+=1
		print(res)

		#fakematrix[fakecount].append(dct)

	#fakecount+=1

#printzigzag(fakematrix)
#################################



