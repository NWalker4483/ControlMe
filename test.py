import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.interpolate import Rbf
varray=cv2.imread('/Users/nile/Downloads/testo.png')
varray=cv2.GaussianBlur(varray,(11,11),7)
#varray=cv2.cvtColor(varray,cv2.COLOR_BGR2GRAY)
print("ok")

varray=np.array([[(np.sin(i)*255) for i in range(500)] for a in range(500)])
lx,ly=varray.shape[0],varray.shape[1]
cv2.imshow('',varray)
cv2.waitKey(0)
vgrad = np.gradient(varray)

mag = vgrad[0]+ vgrad[1]
plt.imshow(mag, vmin = np.amin(mag), vmax=np.amax(mag))
plt.colorbar()
plt.show()  
'''

x, y, z, d = np.random.rand(4, 50)
rbfi = Rbf(x, y, z, d)  # radial basis function interpolator instance
xi = yi = zi = np.linspace(0, 1, 20)
di = rbfi(xi, yi, zi)   # interpolated values
print(di.shape)
'''