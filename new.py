import stream as st
import cv2
import time
import numpy as np
def percent_diff(img1,img2):
    top=abs(np.subtract(img1,img2))
    bot=np.add(img2,img1)/2
    ans=top/bot
    return ans
def get_grid():
    frame= cv2.blur(cam.read(),(5,5))
    frame=st.pixelate(frame,pixelSize=9)
    frame=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    return frame
views=["Test"]
cam=st.ConnectCam()
st.Create_Views(views)

global comp
comp=get_grid()
while True: 
    #frame=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    frame=get_grid()
    try:
        frame=np.multiply(percent_diff(comp,frame),1)
    except:
        pass
    r=st.Update_Views(views,[frame])
    if r>0:
        if chr(r)=='q':
            comp=get_grid()

