#include<AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
uint8_t direct;
byte inByte;
int read_num(int numberOfDigits){
  char theNumberString[numberOfDigits + 1];
  int theNumber;
  for (int i = 0; i < numberOfDigits; theNumberString[i++] = Serial.read());
  theNumberString[numberOfDigits] = 0x00;
  theNumber =   (theNumberString);
  return theNumber;
}
void setup() {
  // put your setup code here, to run once:
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);
}
void loop() {
if (Serial.available())
{
inByte=Serial.read();
switch(Serial.read()) {
   case 'F':
      direct=FORWARD;
      break; /* optional */
   case 'B':
      direct=BACKWARD;
      break; /* optional */
   case 'R':
      direct=RELEASE;
      break; /* optional */

int rate=read_num(3);
Serial.flush();
switch(inByte) {

   case 'A':
      motor1.setSpeed(rate);
      motor1.run(direct);
      break; /* optional */
   case 'B':
      motor2.setSpeed(rate);
      motor2.run(direct);
      break; /* optional */
   case 'C':
      motor3.setSpeed(rate);
      motor3.run(direct);
      break; /* optional */
   case 'D':
      motor4.setSpeed(rate);
      motor4.run(direct);
      break; /* optional */
   /* you can have any number of case statements */
   default : /* Optional */
  motor1.setSpeed(0);
  motor2.setSpeed(0);
  motor3.setSpeed(0);
  motor4.setSpeed(0);   
   break;
}}}}
