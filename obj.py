import cv2
import numpy as np
pos=(100,90)
def make_blob():
    pass
def Merge(src,src2,pos):
    height, width = src.shape[:2]
    for a in range(len(src2)):
        for i in range(len(src2[0])):
            src[pos[1]+a][pos[0]+i]=src2[a][i]
            if i+pos[0] == width-1:
                return src
        if a+pos[1] == height-1:
                return src 
    return src

data=np.array([[i,]*255 for i in range(255)], dtype=np.uint8)
slip=[]
blob=np.array([[i,]*50 for i in range(data[pos[1]][0]+50,255)], dtype=np.uint8)
blob2=np.rot90(np.array([[i,]*50 for i in range(data[pos[1]][0],255,4)], dtype=np.uint8),1, (1,0))
data1=Merge(data,blob,pos)
data1=Merge(data1,blob2,pos)
data=np.rot90(data,1, (1,0))
data1=np.rot90(data1,1, (1,0))
for i in range(len(data)):
    slip.append(np.diff(data1[i])/np.diff(data[i]))
slip=np.array(slip, dtype=np.uint8)
data=np.concatenate((slip, data), axis=1)
#data=np.gradient(data)[1]
#data = np.stack((data,data1), axis=len(data[0].shape))
cv2.imshow("",data)
cv2.waitKey(0)

