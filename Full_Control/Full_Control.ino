
#include<AFMotor.h>
#include <Servo.h>

int rate;
int rdir;
int ldir;
int right;
int left;
//Servo myservo;
//AF_DCMotor motor1(1);
//AF_DCMotor motor2(2);
//AF_DCMotor motor3(3);
//AF_DCMotor motor4(4);
//AF_DCMotor AllMotors[4] = {motor1, motor2, motor3, motor4};
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
    
  //Setup Channel A
  pinMode(12, OUTPUT); //Initiates Motor Channel A pin
  pinMode(9, OUTPUT); //Initiates Brake Channel A pin

  //Setup Channel B
  pinMode(13, OUTPUT); //Initiates Motor Channel A pin
  pinMode(8, OUTPUT);
  
  Serial.begin(9600);
  Serial.println("Initialized");
  // put your setup code here, to run once:
for (int i=0;i<4;i++){
  //AllMotors[i].setSpeed(255);
}
  //myservo.attach(9);
}
void loop() {
if (Serial.available())
{ //myservo.attach(9);
  delay(500);
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
}
rate=read_num(3);
//AllMotors[inByte].setSpeed(rate);
//AllMotors[inByte].run(direct);
}
if (inByte==4){
switch(Serial.read()) {
   case 'F':
      direct=FORWARD;
      digitalWrite(12, HIGH); //Establishes forward direction of Channel A
      digitalWrite(9, LOW);   //Disengage the Brake for Channel A
    
      break; 
   case 'B':
      direct=BACKWARD;
        digitalWrite(12, LOW); //Establishes forward direction of Channel B
        digitalWrite(9, LOW);  //Spins the motor on Channel B at full speed
      break;
   case 'R':
      direct=RELEASE;
      digitalWrite(9, HIGH);
      break;
}
right=read_num(3);
analogWrite(3, rate);
//AllMotors[0].setSpeed(right);
//AllMotors[0].run(direct);
switch(Serial.read()) {
   case 'F':
      direct=FORWARD;
      digitalWrite(13, HIGH); //Establishes forward direction of Channel B
        digitalWrite(8, LOW); 
      break; 
   case 'B':
      direct=BACKWARD;
      digitalWrite(13, LOW); //Establishes forward direction of Channel B
        digitalWrite(8, LOW);  
      break;
   case 'R':
      direct=RELEASE;
       digitalWrite(9, HIGH);
      break;
}
left=read_num(3);
analogWrite(11, rate);
//AllMotors[1].setSpeed(left);
//AllMotors[1].run(direct);

}
Serial.println(left);
Serial.println(right);
}}

