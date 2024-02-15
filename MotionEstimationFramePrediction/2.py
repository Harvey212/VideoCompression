import numpy as np 
from PIL import Image 

############################################
img = Image.open('foreman_qcif_0_rgb.bmp')  
y,cb,cr=img.convert('YCbCr').split()
y1=np.array(y)

blockrows=int(y1.shape[0]/16)
blockcols=int(y1.shape[1]/16)

finalmodes=[]
finalarrs=[]



for i in range(blockrows):
	orirow=16*i
	for j in range(blockcols):
		oricol=16*j
		###################
		comp=np.zeros((16,16))
		n1=0
		for s1 in range(orirow,(orirow+16)):
			n2=0
			for s2 in range(oricol,(oricol+16)):
				comp[n1][n2]=y1[s1][s2]
				n2+=1
			n1+=1
		########
		checklist=[0,0,0,-1,0]
		
		if (orirow-1)<0:
			checklist[0]=-1
			checklist[2]=-1
			checklist[4]=-1

		if (oricol-1)<0:
			checklist[1]=-1
			checklist[2]=-1
			checklist[4]=-1

		

		candymode=-1
		candyarr=np.zeros((16,16))
		diff=np.inf

		#############################
		for m in range(len(checklist)):
			if checklist[m]==0:

				arr=np.zeros((16,16))

				rr=0
				cc=0

				if m==0:
					for h in range(oricol,(oricol+16)):
						now=y1[(orirow-1)][h]
						for rr in range(16):
							arr[rr][cc]=now
						cc+=1
				if m==1:
					for v in range(orirow,(orirow+16)):
						now=y1[v][(oricol-1)]
						for cc in range(16):
							arr[rr][cc]=now
						rr+=1
				if m==2:
					summ=0
					count=0
					for h in range(oricol,(oricol+16)):
						count+=1
						summ+=y1[(orirow-1)][h]
					for v in range(orirow,(orirow+16)):
						count+=1
						summ+=y1[v][(oricol-1)]
					summ=summ/count

					for rr in range(16):
						for cc in range(16):
							arr[rr][cc]=summ

				if m==4:
					now=y1[(orirow-1)][(oricol-1)]
					for rr in range(16):
						arr[rr][rr]=now

					for rr in range(15):
						now=y1[(orirow+rr)][(oricol-1)]
						for cc in range((15-rr)):
							arr[(cc+(rr+1))][cc]=now

					for cc in range(15):
						now=y1[(orirow-1)][(oricol+cc)]
						for rr in range((15-cc)):
							arr[rr][(1+cc)+rr]=now



				dif=0
				for s1 in range(16):
					for s2 in range(16):
						dif+=abs(arr[s1][s2]-comp[s1][s2]) 
				if dif<diff:
					candyarr=arr
					candymode=m
					diff=dif

		###################################
		finalmodes.append(candymode)
		finalarrs.append(candyarr)


collage=np.zeros((y1.shape[0],y1.shape[1]))
count=0
for i in range(blockrows):
	orirow=16*i
	for j in range(blockcols):
		oricol=16*j
		if finalmodes[count]!=-1:
			ans="Block "+str(count)+": "+"mode"+str(finalmodes[count])
			print(ans)

			tar=finalarrs[count]
			s1=0
			for m in range(orirow,(orirow+16)):
				s2=0
				for n in range(oricol,(oricol+16)):
					collage[m][n]=tar[s1][s2]
					s2+=1
				s1+=1
		else:
			for m in range(orirow,(orirow+16)):
				for n in range(oricol,(oricol+16)):
					collage[m][n]=y1[m][n]
		count+=1
		

ress=Image.fromarray(collage)
ress.show()
ress = ress.convert('RGB')
ress.save("2b.jpg")