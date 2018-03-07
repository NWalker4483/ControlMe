import cv2
import datetime
import time
from PIL import Image
import numpy as np
class VideoCamera(object):
    def __init__(self,pixelsize=None):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.pixelsize=pixelsize
        self.capstr="Capturing"
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
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        if self.pixelsize!=None:
            image=self.pixelate(image,self.pixelsize)
        image=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (0,700)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2
        #Add timestamp to frame
        cv2.putText(image,("{0}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H:%M:%S'))), 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
        