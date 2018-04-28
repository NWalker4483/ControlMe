import serial
class Linear_Actuator():
    def __init__(self,path="/dev/ttyACM1",lets='1'):
        self.ratio=255/100
        self.lets=lets
        self.connected=False
        try:
            self.path=serial.Serial(port=path)
            self.connected=True
        except:
            print("Noduino")
    def move(self,dir,goal):
        if self.connected:
            self.path.write((self.lets+ dir +str(int(goal*self.ratio)).encode('utf-8')))
    def direct(self,num):
        return "F" if num>0 else "B"
    def drive(self,right,left):
        if self.connected:
            print(('4'+ self.direct(right)+str(abs(right))+ self.direct(left)+str(abs(left))))
            self.path.write(('4'+ self.direct(right)+str(abs(right)).rjust(3,'0')+ self.direct(left)+str(abs(left)).rjust(3,'0')).encode('utf-8'))

if __name__=="__main__":
    test=Linear_Actuator()
    while True:
        test.move(int(input()),255)
    test.path.close()