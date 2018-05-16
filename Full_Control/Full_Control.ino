
#include<AFMotor.h>
#include "SoftwareSerial.h"
#define SpeedLength 3
#define rxPin 2  // pin 3 connects to smcSerial TX  (not used in this example)
#define RightMotor 4  // Serial or PWM Transimission Pin on Arduino 
#define LeftMotor 3  // Serial or PWM Transimission Pin on Arduino 
#define LiftArm 5  // Serial Transimission Pin on Arduino 
#define Dump_Lower 9  // Serial Transimission Pin on Arduino 
#define Dump_Limiter_Low 12
#define Dump_Limiter 11  // Limiter Read Pin on Arduino 
#define Dump_Upper 10  // Serial Transimission Pin on Arduino 
#define Scoop 6 // PWM Out Pin on Arduino 
#define txPin 4


SoftwareSerial AllMotors[4] = {SoftwareSerial(rxPin, 11),
SoftwareSerial(rxPin, 10),
SoftwareSerial(rxPin, LiftArm), 
SoftwareSerial(rxPin, Dump_Upper), 
SoftwareSerial(rxPin, Dump_Lower), 
SoftwareSerial(rxPin, txPin)};

int direct;
int rate;
int motor;
byte inByte;
     // Motor connected to digital pin 9

//Read Direction and speed indicator from Serial
void Drive(int y,int val){
  if (val<=0){
 digitalWrite(y,HIGH);
   }
  else{
    digitalWrite(y,LOW);
  }
}

//sets the new target for the JRK21V3 controller, this uses pololu high resulution protocal
void Move(int x,int _motor) {
  if (x>0){
  word target = int(x*(4098/255));  
  }
  else{
    word target = int(x*(2048/255));  
  }//only pass this ints, i tried doing math in this and the remainder error screwed something up
  AllMotors[_motor].write(0xAA); //tells the controller we're starting to send it commands
  AllMotors[_motor].write(0xB);   //This is the pololu device # you're connected too that is found in the config utility(converted to hex).
  AllMotors[_motor].write(0x40 + (target & 0x1F)); //first half of the target, see the pololu jrk manual for more specifics
  AllMotors[_motor].write((target >> 5) & 0x7F);   //second half of the target, " " "
}  
int get_speed(){
  switch(Serial.read()) {
   case 'F':
      rate=read_num(SpeedLength);
      break; 
   case 'B':
      rate=read_num(SpeedLength)*-1;
      break;
   case 'R':
      rate=0;
      break;
  default:
      rate=read_num(SpeedLength);
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

/*InByte dictionary 
0:Drive Train 
2:Lift Arm
3:Scoop
4:Dump
*/
void setSimpleMotorSpeed(int _speed, int motor)
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
  pinMode(Dump_Limiter, INPUT);  
  pinMode(Scoop, OUTPUT); 
  pinMode(RightMotor,OUTPUT);
  pinMode(LeftMotor,OUTPUT);  // sets the pin as output
  digitalWrite(RightMotor,HIGH);
  digitalWrite(Scoop,HIGH);
  digitalWrite(LeftMotor,HIGH);

for (int i=0;i<sizeof(AllMotors)/sizeof(AllMotors[0]);i++){
  AllMotors[i].begin(9600);//19200);//Baud-Rate
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
  delay(5);
inByte=read_num(1);
switch (inByte ){
case 0:

setSimpleMotorSpeed(get_speed(),0);
setSimpleMotorSpeed(get_speed(),1);

break;
case 1:
analogWrite(RightMotor,get_speed()%255);
analogWrite(LefttMotor,get_speed()%255);
case 2: 
Move(get_speed(),2);
break;
case 3:
analogWrite(Scoop,get_speed()%255);
break;
case 4:
Move(get_speed(),4);
break;
case 5:
Move(get_speed(),3);
break;
case 6:
Drive(RightMotor,get_speed()%255);
case 7:
Drive(LefttMotor,get_speed()%255);
default:
analogWrite(inByte,get_speed()%255);
break;
}
//Serial.println(left);
//Serial.println(right);
}}

