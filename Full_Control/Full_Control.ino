
#include<AFMotor.h>
#include "SoftwareSerial.h"
#define rxPin 8  // pin 3 connects to smcSerial TX  (not used in this example)
#define RightMotor 4  // pin 3 connects to smcSerial RX  (not used in this example)
#define LeftMotor 3  // pin 3 connects to smcSerial RX  (not used in this example)
#define LiftArm 5
#define txPin 4
// pin 4 connects to smcSerial RX
int rate;
SoftwareSerial motor1 = SoftwareSerial(rxPin, RightMotor);
SoftwareSerial motor2 = SoftwareSerial(rxPin, LeftMotor);
SoftwareSerial motor3 = SoftwareSerial(rxPin, LiftArm);
SoftwareSerial motor4 = SoftwareSerial(rxPin, txPin);
SoftwareSerial AllMotors[4] = {motor1, motor2, motor3, motor4};
int direct;
int motor;
byte inByte;
int get_speed(){
  switch(Serial.read()) {
   case 'F':
      rate=read_num(4);
      break; 
   case 'B':
      rate=read_num(4)*-1;
      break;
   case 'R':
      rate=0;
      break;
}
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
void setMotorSpeed(int speed,int motor)
{
  if (speed < 0)
  {
    AllMotors[motor].write(0x86);  // motor reverse command
    speed = -speed;  // make speed positive
  }
  else
  {
    motor.write(0x85);  // motor forward command
  }
  AllMotors[motor].write(speed & 0x1F);
  AllMotors[motor].write(speed >> 5);
}
void setup() {
  Serial.begin(9600);
  Serial.println("Initialized");
  // put your setup code here, to run once:
for (int i=0;i<4;i++){
  AllMotors[i].begin(19200);
  delay(5);
  AllMotors[i].write(0xAA);
  AllMotors[i].write(0x83);
} 
delay(5);
  //myservo.attach(9);
}
void loop() {
if (Serial.available())
{ //myservo.attach(9);
  delay(50);
inByte=read_num(1);
if (inByte <= 1){
setMotorSpeed(get_speed,inByte);
setMotorSpeed(get_speed,inByte);
}
else {
setMotorSpeed(get_speed,inByte);

}
//Serial.println(left);
//Serial.println(right);
}}

