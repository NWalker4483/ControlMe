import cv2
import time
import numpy as np
import datetime
from imutils.video import VideoStream
import imutils
def Create_Views(windows,pos=(0,0)):#list of window names
    for i in windows:
        #Create Windows to view images
        cv2.namedWindow(i, cv2.WINDOW_AUTOSIZE)  
        cv2.moveWindow(i,0,0)  
    #Start the window thread for the two windows we are using
    cv2.startWindowThread()
#Position the windows next to eachother
def Update_Views(names,images):
    for i in zip(names,images):
        cv2.imshow(i[0],i[1])#name,image
    return cv2.waitKey(1)
def ConnectCam(pi=False):
    time.sleep(1)
    # initialize the video stream and allow the cammera sensor to warmup
    return VideoStream(usePiCamera=pi).start()
    
def Log_Image(name,image):
    cv2.imwrite("{0}{1}.png".format(name,datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H:%M:%S')),image)

def pixelate(_image,pixelSize=32):
    from PIL import Image
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


def random_mask(data, frac=0.05):
    N = data.size
    frac = np.int(frac * N)
    #FIXME: Must excluded the land mask, so frac has a real meaning!
    idx = np.random.random_integers(0, N-1, frac)
    return idx

def mask_data(data, idx):
    out = data.copy()
    i, j = np.unravel_index(idx, data.shape)
    out[i, j] = 0
    return ma.masked_equal(out, 0)
if __name__=="__main__":
    import numpy.ma as ma
    camera=ConnectCam()
    views=["Test"]
    Create_Views(views)
    from gridfill import fill
    kw = dict(eps=1e-4, relax=0.6, itermax=1e4, initzonal=False,cyclic=False, verbose=False)
    while True:
        key = cv2.waitKey(1) & 0xFF
        img=cv2.cvtColor(camera.read(),cv2.COLOR_BGR2GRAY)

        idx = random_mask(img, frac=0.05)
        img = mask_data(img, idx)
       

        img, _ = fill(img, 1, 0, **kw)
        print(len(img),len(img[0]))
        img = np.array([[int(img[a][i]) for i in range(len(img[0]))]for a in range(len(img))], dtype=np.uint8)
        print(*img[0])
        if key=='q':
            Log_Image("Test",img)
        #Update_Views(views,[img])
    camera.release()
    cv2.destroyAllWindows()



#Start the window thread for the two windows we are using

