1import serial
class Linear_Actuator():
    def __init__(self,path="/dev/ttyACM",lets='1'):
        self.ratio=255/100
        self.connected=False
        for i in range(4):
            try:
                self.path=serial.Serial(port=path+str(i))
                self.connected=True
                break
            except:
                pass
        if self.connected!=True:
                print("Noduino")
       
             
    def move(self,lets,goal,dir='N'):
        if self.connected:
            self.path.write((str(lets)+ dir +str(int(goal*self.ratio))).encode('utf-8'))
    def direct(self,num):
        return "F" if num>0 else "B"
    def drive(self,right,left):
        if self.connected:
            print(('0'+ self.direct(right)+str(abs(right))+ self.direct(left)+str(abs(left))))
            self.path.write(('0'+ self.direct(right)+str(abs(right)).rjust(4,'0')+ self.direct(left)+str(abs(left)).rjust(4,'0')).encode('utf-8'))

if __name__=="__main__":
    test=Linear_Actuator()
    while True:
        test.move(int(input()),3200)
    test.path.close()