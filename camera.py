import cv2
import datetime
import time
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.capstr="Capturing"
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (0,700)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2
        cv2.putText(image,("{0}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H:%M:%S'))), 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
        