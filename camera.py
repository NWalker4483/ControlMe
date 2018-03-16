import cv2
import datetime
import time
from PIL import Image
import numpy as np
try:
    import freenect
except:
    print('No Kinect')

class VideoCamera(object):
    def __init__(self,kinect=False,pixelsize=None):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.pixelsize=pixelsize
        self.capstr="Capturing"
        self.kinect=kinect
        if kinect:
            import freenect
            self.video=freenect
        else:
            self.video = cv2.VideoCapture(0)
            self.video.set(3,640)
            self.video.set(4,480)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    def pixelate(self,_image,pixelSize=32):
        backgroundColor = (0,)*3
        _image = cv2.flip(_image,1)
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
    def __del__(self):
        pass
        #self.video.release()
    
    def make_gamma(self):
        """
        Create a gamma table
        """
        num_pix = 2048 # there's 2048 different possible depth values
        npf = float(num_pix)
        _gamma = np.empty((num_pix, 3), dtype=np.uint16)
        for i in range(num_pix):
            v = i / npf
            v = pow(v, 3) * 6
            pval = int(v * 6 * 256)
            lb = pval & 0xff
            pval >>= 8
            if pval == 0:
                a = np.array([255, 255 - lb, 255 - lb], dtype=np.uint8)
            elif pval == 1:
                a = np.array([255, lb, 0], dtype=np.uint8)
            elif pval == 2:
                a = np.array([255 - lb, lb, 0], dtype=np.uint8)
            elif pval == 3:
                a = np.array([255 - lb, 255, 0], dtype=np.uint8)
            elif pval == 4:
                a = np.array([0, 255 - lb, 255], dtype=np.uint8)
            elif pval == 5:
                a = np.array([0, 0, 255 - lb], dtype=np.uint8)
            else:
                a = np.array([0, 0, 0], dtype=np.uint8)

            _gamma[i] = a
        return _gamma
    def filter(self,image,depth):
        hsv = cv2.cvtColor(depth, cv2.COLOR_BGR2HSV)
        lower_red = np.array([12,22,121])
        upper_red = np.array([255,255,180])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        image = cv2.bitwise_and(image, image, mask = mask)
        return image


    def get_frame(self,depth=False):
        if self.kinect and depth==False:
            image,_ = freenect.sync_get_video()
        if depth:
            depth,_ = freenect.sync_get_depth() # get the depth readinngs from the camera
            image = self.make_gamma()[depth].astype(np.uint8) 
            image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
            image=self.filter(freenect.sync_get_video()[0],image)
            
            
        else:
            success, image = self.video.read()
        if self.pixelsize!=None:
            image=self.pixelate(image,self.pixelsize)
        #image=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (0,700)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2
        #Add timestamp to frame
        '''
        cv2.putText(image,("{0}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H:%M:%S'))), 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)'''
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
        