/*+++++++++++++++++++++++++++++++++++++++++++++++++++
Author      : Fahmi Ghani
Date        : 11 July 2015 
printoject     : Joystick control differential drive dc motor robot
Component   : Analog Joystick
              2Amp motor driver shield
              DC Motor
Description : Control DC motor direction using Joystick
Video :https://www.youtube.com/watch?v=kfT3eoNAM-Q
+++++++++++++++++++++++++++++++++++++++++++++++++++*/

//Set pin numbers:
const byte joyStickYPin = A2;
const byte joyStickXPin = A1;
const byte motorLSpeedPin = 5;
const byte motorLDirPin = 4;
const byte motorRSpeedPin = 6;
const byte motorRDirPin = 7;

//variables
//Joystick input variables
 joyXValue = 0;
 joyYValue = 0;
 joyValueMax = 2000;
 joyValueMin = 1000;
 joyValueMid = 1500;
 joyValueMidUpper = joyValueMid + 100;
 joyValueMidLower = joyValueMid - 100;

//DC motor variables
 speedFwd = 0;
 speedTurn = 0;
 speedLeft = 0;
 speedRight = 0;


byte motorSpeed = 0;
byte motorSpeedMax = 255;
byte motorSpeedMin = 90; //set to smallest value that make motor move (default 0)
                         // DC motor that I use start to move at 90 pwm value
def map(x,input_start,input_end,output_start,output_end):
    return (x - input_start) / (input_end - input_start) * (output_end - output_start) + output_start


void loop() 
{
   // joyXValue = analogRead(joyStickXPin); //Turn
   // joyYValue = analogRead(joyStickYPin); //Forward/backward
    
    joyXValue = int(input())
    joyYValue = pulseIn(joyStickYPin,HIGH);
    
    if(joyYValue > joyValueMidUpper)//forward
    {
        speedFwd = map(joyYValue, joyValueMidUpper, joyValueMax, motorSpeedMin, motorSpeedMax);
    }
    else if(joyYValue < joyValueMidLower) //backward
    {
        speedFwd = map(joyYValue, joyValueMidLower, joyValueMin, -motorSpeedMin, -motorSpeedMax);
    }
    else 
    {
       speedFwd =0;
    }
    
    if(joyXValue > joyValueMidUpper) //right
    {
        speedTurn = map(joyXValue, joyValueMidUpper, joyValueMax, motorSpeedMin, motorSpeedMax);
    }
    else if(joyXValue < joyValueMidLower) //left
    {
        speedTurn = map(joyXValue, joyValueMidLower, joyValueMin, -motorSpeedMin, -motorSpeedMax);
    }
    else 
    {
       speedTurn =0;
    }

    speedLeft = speedFwd + speedTurn;
    speedRight = speedFwd - speedTurn;

    speedLeft = constrain(speedLeft, -255, 255);
    speedRight = constrain(speedRight, -255, 255);
    
    MoveRobot(speedLeft,speedRight);
  
    print(speedFwd);
    print("\t" );
    print(speedTurn);
    print("\t" );
    print(speedLeft);
    print("\t" );
    print(speedRight);
    Serial.println(" ");
    
    delay(100);

}

def MoveRobot( spdL,  spdR):
{
     if(spdL>0)
     {
        digitalWrite(motorLDirPin, HIGH);
     }
     else
     {
        digitalWrite(motorLDirPin, LOW);
     }
     if(spdR>0)
     {
        digitalWrite(motorRDirPin, HIGH);
     }
     else
     {
        digitalWrite(motorRDirPin, LOW);
     }
     
     analogWrite(motorLSpeedPin, abs(spdL));
     analogWrite(motorRSpeedPin, abs(spdR));     
}