import serial
class Linear_Actuator():
    def __init__(self,path="/dev/ttyACM0",lets='A'):
        self.ratio=255/100
        self.lets=lets
        self.path=serial.Serial(port=path) 
    def move(self,dir,goal):
        pass
        self.path.write((self.lets+ dir +str(int(goal*self.ratio)).encode('utf-8')))

if __name__=="__main__":
    test=Linear_Actuator()
    while True:
        test.move(int(input()),255)
    test.path.close()