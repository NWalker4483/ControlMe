
import serial
class Linear_Actuator():
    def __init__(path="/dev/ttyACM0"):
        self.ratio=4095/100
        self.path=serial.Serial(port=path) 
    def move(self,goal):
        self.path.write(("#"+int(goal*self.ratio).encode('utf-8'))

if __name__=="__main__":
test=Linear_Actuator('/dev/ttyACM0')
    while True:
        test.move(int(input()))
    test.path.close()