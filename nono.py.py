import cv2
import numpy as np
from scipy.ndimage.morphology import binary_closing

def pixelate(_image,pixelSize=32):
    from PIL import Image
    backgroundColor = (0,)*3
    #_image = cv2.flip(_image,1)
    _image=Image.fromarray(_image)
    _image = _image.resize((int(_image.size[0]/pixelSize), int(_image.size[1]/pixelSize)), Image.NEAREST)
    _image = _image.resize((int(_image.size[0]*pixelSize), int(_image.size[1]*pixelSize)), Image.NEAREST)
    """
    pixel=_image.load()
    for i in range(0,_image.size[0],pixelSize):
        for j in range(0,_image.size[1],pixelSize):
            for r in range(pixelSize):
                pixel[i+r,j] = backgroundColor
                pixel[i,j+r] = backgroundColor
                """
    return np.array(_image)
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
def nothing(one):
    pass
# create trackbars for color change
cv2.createTrackbar('H1','image',0,255,nothing)
cv2.createTrackbar('S1','image',0,255,nothing)


# create switch for ON/OFF functionality

    # get current positions of four trackbars
def gen():
    import imutils
    cap = cv2.VideoCapture('/Users/nile/Downloads/lane-detection-with-opencv-master/drivevideo.mp4')
    frame_counter = 0
    while(cap.isOpened()):
        
        ret, frame = cap.read()
        frame=imutils.resize(frame,width=300,height=300)
        r = frame.copy()
        # set blue and green channels to 0
        r[:, :, 0] = 0
        r[:, :, 1] = 0
        frame=cv2.cvtColor(r,cv2.COLOR_RGB2GRAY)
        #ret, mask = cv2.threshold(frame, 125, 255, cv2.THRESH_BINARY)
        if ret:
            #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h1 = cv2.getTrackbarPos('H1','image')
            s1 = cv2.getTrackbarPos('S1','image')
            _,mask = cv2.threshold(frame, 125, 255, cv2.THRESH_BINARY)

            #mask=pixelate(cv2.blur(mask,(6,6)),16)
            
            #mask=cv2.resize(mask, (frame.shape[:2][::-1]), interpolation = cv2.INTER_AREA)
            #
            #mask=np.array(mask, dtype=np.uint8)
            #mask= binary_closing(mask, structure=np.ones((6,3)))
            mask=np.array(mask, dtype=np.uint8)*255
            #çprint(mask)
            #mask=pixelate(cv2.blur(mask,(6,6)),32)
            #mask=cv2.resize(mask, (frame.shape[:2][::-1]), interpolation = cv2.INTER_AREA)
           # ret, mask = cv2.threshold(mask, 125, 255, cv2.THRESH_BINARY)
            #print(mask.shape,(frame.shape[:2]))
            res = cv2.bitwise_and(frame,frame, mask= mask)


        
            cv2.imshow('image',res)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        else:
            print('no video')
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    return gen()
gen()
cv2.destroyAllWindows()
cap.release()
#006 000 105

#127 29 201