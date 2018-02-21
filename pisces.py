# This program will let you test your ESC and brushless motor with a raspberry pi.
# Modification by Nile Walker based on/inspired from ESC.py by AGT @instructable.com

import os, sys   #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library
from getch import getch
import itertools
import threading
pi = pigpio.pi()

class ESC():
    def __init__(self,pin,max_value = 2000,min_value = 700,speed=0,calibrated=False):
        self.pin=pin
        self.max_value=max_value
        self.min_value=min_value
        self.ratio=(min_value-max_value)/100
        self.calibrated=calibrated
        if(min_value<=speed<=max_value):
            self.speed = speed
            self.update()
        else:
            print("Either no speed was given or given speed is either above or below the allowed range and has been set to minimum")
            self.speed = 0
        if calibrated == False:
            self.calibrate()
            
    def manual_drive(self): #You will use this function to program your ESC if required
        print("You have selected manual option so give a value between 0 and 100 type 'stop' to exit")  
        while True:
            inp = 0#raw_input()
            if inp == "stop":
                self.stop()
                break
            else:
                self.update(inp)
                    
    def calibrate(self):   #This is the auto calibration procedure of a normal ESC
        self.update(0)
        print("Disconnect the battery and press enter")
        self.Loading(1)
        inp = 0#raw_input()
        if inp == '':
            self.update(100)
            print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
            inp = 0#raw_input()
            if inp == '':            
                self.update(0)
                print ("Special tone")
                self.Loading(7)
                print ("Wait for it ....")
                self.Loading(5)
                print ("Im working on it.....")
                self.update(0)
                self.Loading(2)
                print ("Arming ESC now...")
                self.update(0)
                self.calibrated=True 
                self.arm()
                print ("ESC Calibrated and Armed")
                
    def test_control(self): 
        print ("Starting the motor...")
        self.Loading(1)
        # change your speed if you want to.... it should be between 700 - 2000
        print ("Controls x to stop - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
        while True:
            inp = getch()
            if inp == "q":
                self.speed -= 10   # decrementing the speed 
            elif inp == "e":    
                self.speed += 10    # incrementing the speed 
            elif inp == "d":
                self.speed += 1    # incrementing the speed 
            elif inp == "a":
                self.speed -= 1     # decrementing the speed
            elif inp == "x":
                print("Stopping...")
                self.stop()     #going for the stop function
                break
            else:
                print ("Press a,q,d or e")
            self.update()
            print ("speed = {0}".format(self.speed))
    def arm(self): #This is the arming procedure of an ESC 
        self.update(0)
        self.Loading(1)
        self.update(100)
        self.Loading(1)
        self.update(0)
        self.Loading(1)
        
    def stop(self): #This will stop every action your Pi is performing for ESC ofcourse.
        self.update(0)
        print("Stopping...")
        pi.stop()
    def update(self,_speed=None):
        _speed=self.speed if _speed==None else _speed
        #pi.set_servo_pulsewidth(self.pin,self.ratio*_speed)
        print(self.speed)
        self.speed=_speed
    def Loading(self,wait):
        done = False 
        def play(_wait): 
            for c in itertools.cycle(['|', '/', '-', '\\']):
                if done:
                    break
                sys.stdout.write('\rself.Loading ' + c)
                sys.stdout.flush()
                time.sleep(0.1)
        t = threading.Thread(target=play,args=(wait,))
        t.start()
        time.sleep(wait)
        done = True

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--pin", type=int,
                        help="BCM pin value for your ESC's signal wire")
    parser.add_argument("-s", "--speed", type=int,
                        help="set output speed")
    args = parser.parse_args()
    #This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.    
    if type(args.speed)!=None and type(args.pin)!=None:
        Test=ESC(args.pin,speed=args.speed,calibrated=True)
        Test.test_control()
    elif type(args.pin)!=None:
        Test=ESC(args.pin)
        Test.test_control()
    else:
        print("Error No Pin Value Supplied")
    
