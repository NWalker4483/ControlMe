

#variables
#Joystick input variables
 joyXValue = 0 
 joyYValue = 0 
 joyValueMax = 100 
 joyValueMin = -100 
 joyValueMid = 0 
 joyValueMidUpper = joyValueMid + 50 
 joyValueMidLower = joyValueMid - 50 

#DC motor variables
 speedFwd = 0 
 speedTurn = 0 
 speedLeft = 0 
 speedRight = 0 


motorSpeed = 0 
motorSpeedMax = 255 
motorSpeedMin = 90  # #set to smallest value that make motor move (default 0)
                        #  # DC motor that I use start to move at 90 pwm value
def constrain(val, min_val, max_val):

    if val < min_val: return min_val
    if val > max_val: return max_val
    return val
def map(x,input_start,input_end,output_start,output_end):
    return (x - input_start) / (input_end - input_start) * (output_end - output_start) + output_start


while True:
   # joyXValue = analogRead(joyStickXPin)   #Turn
   # joyYValue = analogRead(joyStickYPin)   #Forward/backward
    
    joyXValue = int(input())
    joyYValue = int(input())
    
    if(joyYValue > joyValueMidUpper): #forward
        speedFwd = map(joyYValue, joyValueMidUpper, joyValueMax, motorSpeedMin, motorSpeedMax) 
    elif(joyYValue < joyValueMidLower):  #backward
        speedFwd = map(joyYValue, joyValueMidLower, joyValueMin, -motorSpeedMin, -motorSpeedMax) 
    else:    
       speedFwd =0 

    
    if(joyXValue > joyValueMidUpper):  #right
        speedTurn = map(joyXValue, joyValueMidUpper, joyValueMax, motorSpeedMin, motorSpeedMax) 
    elif(joyXValue < joyValueMidLower):  #left
        speedTurn = map(joyXValue, joyValueMidLower, joyValueMin, -motorSpeedMin, -motorSpeedMax) 
    else:
       speedTurn =0 

    speedLeft = speedFwd + speedTurn 
    speedRight = speedFwd - speedTurn 

    speedLeft = constrain(speedLeft, -255, 255) 
    speedRight = constrain(speedRight, -255, 255) 
    
    #MoveRobot(speedLeft,speedRight) 
  
    print(speedFwd) 
    print(" ") 
    print(speedTurn) 
    print(" " ) 
    print(speedLeft) 
    print(" " ) 
    print(speedRight) 
    print(" ") 
    
'''
def MoveRobot( spdL,  spdR):
{
     if(spdL>0)
     {
        digitalWrite(motorLDirPin, HIGH) 
     }
     else
     {
        digitalWrite(motorLDirPin, LOW) 
     }
     if(spdR>0)
     {
        digitalWrite(motorRDirPin, HIGH) 
     }
     else
     {
        digitalWrite(motorRDirPin, LOW) 
     }
     
     analogWrite(motorLSpeedPin, abs(spdL)) 
     analogWrite(motorRSpeedPin, abs(spdR))      
}'''