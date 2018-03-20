
import cv2
import numpy as np
from matplotlib import pyplot as plt

img0=cv2.imread('/Users/nile/Downloads/testo.png')
# loading image
#img0 = cv2.imread('SanFrancisco.jpg',)

# converting to gray scale
gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
#gray=cv2.Canny(gray,50,200)
# remove noise
img = cv2.GaussianBlur(gray,(31,31),1,1)
img=gray
# convolute with proper kernels
#laplacian = cv2.Laplacian(img,cv2.CV_64F)
vgrad=np.gradient(gray)
mag = np.sqrt(vgrad[0]**2 + vgrad[1]**2)
cv2.imshow("l",gray)
cv2.waitKey(0)
#sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)  # x
#sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)  # y
#xsobely = cv2.Canny(sobely,100,200)

plt.imshow(mag,cmap=plt.get_cmap('hot'), vmin = np.amin(mag),vmax = np.amax(mag))  
plt.colorbar()
plt.show()  