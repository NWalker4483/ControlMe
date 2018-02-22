/*
* Motor control setup for pololu jrk21v3 with Arduino UNO R3, verified using linear actualtor LACT2P
*
* Pololu jrk config utility in Serial mode using UART detect baud rate interface. 
* starting with the default configuration settings for LACT2P linear actuators provided on the pololu website
*
* pin 8 connected to jrk pin Rx
* jrk grnd connected to arduino ground
*/
import serial
class Linear_Actuator()'/dev/ttyACM0'
    def __init__(target,path='/dev/ttyACM0'):
        self.target=target
        self.path=serial.Serial(path) 
    def move(self,goal):
        self.path.write(("#"+goal).encode('utf-8'))
