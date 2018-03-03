/*+++++++++++++++++++++++++++++++++++++++++++++++++++
Author      : Fahmi Ghani
Date        : 11 July 2015 
Project     : Joystick control differential drive dc motor robot
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
int joyXValue = 0;
int joyYValue = 0;
int joyValueMax = 2000;
int joyValueMin = 1000;
int joyValueMid = 1500;
int joyValueMidUpper = joyValueMid + 100;
int joyValueMidLower = joyValueMid - 100;

//DC motor variables
int speedFwd = 0;
int speedTurn = 0;
int speedLeft = 0;
int speedRight = 0;


byte motorSpeed = 0;
byte motorSpeedMax = 255;
byte motorSpeedMin = 90; //set to smallest value that make motor move (default 0)
                         // DC motor that I use start to move at 90 pwm value

void setup() 
{
    Serial.begin(9600);
    Serial.print("START" );
     
    pinMode(joyStickXPin, INPUT);
    pinMode(joyStickYPin, INPUT);
    pinMode(motorLSpeedPin, OUTPUT);
    pinMode(motorLDirPin, OUTPUT);
    pinMode(motorRSpeedPin, OUTPUT);
    pinMode(motorRDirPin, OUTPUT);
}

void loop() 
{
   // joyXValue = analogRead(joyStickXPin); //Turn
   // joyYValue = analogRead(joyStickYPin); //Forward/backward
    
    joyXValue = pulseIn(joyStickXPin,HIGH);
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
  
    Serial.print(speedFwd);
    Serial.print("\t" );
    Serial.print(speedTurn);
    Serial.print("\t" );
    Serial.print(speedLeft);
    Serial.print("\t" );
    Serial.print(speedRight);
    Serial.println(" ");
    
    delay(100);

}

void MoveRobot(int spdL, int spdR) 
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