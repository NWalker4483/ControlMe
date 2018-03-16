
#include<AFMotor.h>
#include <Servo.h>

Servo myservo;
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
AF_DCMotor AllMotors[4] = {motor1, motor2, motor3, motor4};
uint8_t direct;
byte inByte;
//Convert Serial input in to an integer value: given number of digits
int read_num(int numberOfDigits){
  char theNumberString[numberOfDigits + 1];
  int theNumber;
  for (int i = 0; i < numberOfDigits; theNumberString[i++] = Serial.read());
  theNumberString[numberOfDigits] = 0x00;
  theNumber = atoi(theNumberString);
  return theNumber;
}
int* get_RL(int joyXValue,int joyYValue){
    int joyValueMax = 100; 
    int joyValueMin = -100; 
    int joyValueMid = 0;
    int joyValueMidUpper = joyValueMid + 10;
    int joyValueMidLower = joyValueMid - 10;

    //DC motor variables
    int speedFwd = 0;
    int speedTurn = 0;
    int speedLeft = 0;
    int speedRight = 0; 

    int motorSpeed = 0;
    int motorSpeedMax = 255; 
    int motorSpeedMin = 45;  //set to smallest value that make motor move (default 0)
                            // DC motor that I use start to move at 90 pwm value  
    if(joyYValue > joyValueMidUpper){//forward
        speedFwd = map(joyYValue, joyValueMidUpper, joyValueMax, motorSpeedMin, motorSpeedMax); 
     } else if(joyYValue < joyValueMidLower){ //backward
        speedFwd = map(joyYValue, joyValueMidLower, joyValueMin, -motorSpeedMin, -motorSpeedMax) ;
     }
    else{
       speedFwd =0 ;
    }
    
    if(joyXValue > joyValueMidUpper){  //right
        speedTurn = map(joyXValue, joyValueMidUpper, joyValueMax, motorSpeedMin, motorSpeedMax); 
    }
    else if(joyXValue < joyValueMidLower){//left
        speedTurn = map(joyXValue, joyValueMidLower, joyValueMin, -motorSpeedMin, -motorSpeedMax);
        }
    else{
       speedTurn = 0 ;
    }
    speedLeft = speedFwd + speedTurn;
    speedRight = speedFwd - speedTurn;

    speedLeft = constrain(speedLeft, -255, 255);
    speedRight = constrain(speedRight, -255, 255);
    int* xy = malloc(sizeof(int) * 2);
    xy[0]=speedLeft;
    xy[1]=speedRight;
    return xy;
}
void setup() {
  // put your setup code here, to run once:
for (int i=0;i<4;i++){
  AllMotors[i].setSpeed(255);
}
  myservo.attach(9);
  myservo2.attach(10);
}
void loop() {
if (Serial.available())
{
inByte=read_num(1);
if (inByte < 4){
//Read the direction of the actuator
switch(Serial.read()) {
   case 'F':
      direct=FORWARD;
      break; 
   case 'B':
      direct=BACKWARD;
      break;
   case 'R':
      direct=RELEASE;
      break;
int rate=read_num(3);
AllMotors[inByte-1].setSpeed(rate);
AllMotors[inByte-1].run(direct);
}

}
if (inByte==4){

}

}}