import serial
class Linear_Actuator():
    def __init__(self,path="/dev/ttyACM0",lets='1'):
        self.ratio=255/100
        self.lets=lets
        self.connected=False
        try:
            self.path=serial.Serial(port=path) 
        except:
            print("Noduino")
    def move(self,dir,goal):
        if self.connected:
            self.path.write((self.lets+ dir +str(int(goal*self.ratio)).encode('utf-8')))

if __name__=="__main__":
    test=Linear_Actuator()
    while True:
        test.move(int(input()),255)
    test.path.close()