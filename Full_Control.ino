
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
int right=read_num(3);
int left=read_num(3);

}

}}