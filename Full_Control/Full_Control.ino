
#include<AFMotor.h>
#include "SoftwareSerial.h"
#define rxPin 8  // pin 3 connects to smcSerial TX  (not used in this example)
#define RightMotor 4  // pin 3 connects to smcSerial RX 
#define LeftMotor 3  // pin 3 connects to smcSerial RX  
#define LiftArm 5
#define Scoop 6
#define txPin 4
// pin 4 connects to smcSerial RX// RX, TX, plug your control line into pin 8 and connect it to the RX pin on the JRK21v3

//sets the new target for the JRK21V3 controller, this uses pololu high resulution protocal

SoftwareSerial motor1 = SoftwareSerial(rxPin, RightMotor);
SoftwareSerial motor2 = SoftwareSerial(rxPin, LeftMotor);
SoftwareSerial motor3 = SoftwareSerial(rxPin, LiftArm);
SoftwareSerial motor4 = SoftwareSerial(rxPin, txPin);
SoftwareSerial AllMotors[4] = {motor1, motor2, motor3, motor4};
int direct;
int rate;
int motor;
byte inByte;
     // Motor connected to digital pin 9

//Read Direction and speed indicator from Serial
void Move(int x) {
  word target = x;  //only pass this ints, i tried doing math in this and the remainder error screwed something up
  AllMotors[2].write(0xAA); //tells the controller we're starting to send it commands
  AllMotors[2].write(0xB);   //This is the pololu device # you're connected too that is found in the config utility(converted to hex). I'm using #11 in this example
  AllMotors[2].write(0x40 + (target & 0x1F)); //first half of the target, see the pololu jrk manual for more specifics
  AllMotors[2].write((target >> 5) & 0x7F);   //second half of the target, " " "
}  
int get_speed(){
  switch(Serial.read()) {
   case 'F':
      rate=read_num(3);
      break; 
   case 'B':
      rate=read_num(3)*-1;
      break;
   case 'R':
      rate=0;
      break;
}
Serial.println(rate);
return rate;
  }
//Convert Serial input in to an integer value: given number of digits
int read_num(int numberOfDigits){
  char theNumberString[numberOfDigits + 1];
  int theNumber;
  for (int i = 0; i < numberOfDigits; theNumberString[i++] = Serial.read());
  theNumberString[numberOfDigits] = 0x00;
  theNumber = atoi(theNumberString);
  return theNumber;
}
void setMotorSpeed(int _speed, int motor)
{
  
  if (_speed < 0)
  {
    AllMotors[motor].write(0x86);  // motor reverse command
    _speed = -1*_speed;  // make speed positive
  }
  else
  {
    AllMotors[motor].write(0x85);  // motor forward command
  }
  
  AllMotors[motor].write(_speed & 0x1F);
  AllMotors[motor].write(_speed >> 5);
}
void setup() {
  Serial.begin(9600);
  Serial.println("Initialized");
  // put your setup code here, to run once:
 pinMode(Scoop, OUTPUT);   // sets the pin as output

for (int i=0;i<4;i++){
  AllMotors[i].begin(9600);//19200);
  delay(5);
  AllMotors[i].write(0xAA);
  //AllMotors[i].write(0x83);
} 
delay(50);
  //myservo.attach(9);
}
void loop() {
if (Serial.available())
{ //myservo.attach(9);
  delay(50);
inByte=read_num(1);
if (inByte == 0){
setMotorSpeed(get_speed(),0);
setMotorSpeed(get_speed(),1);
}
else {
  if (inByte==3)
  {analogWrite(Scoop,abs(get_speed())%255);
  }
  if (inByte==2)
  {Move(get_speed());
  }
  else{
setMotorSpeed(get_speed(),inByte);
  }
}
//Serial.println(left);
//Serial.println(right);
}}

