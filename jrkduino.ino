
#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
int read_num(int numberOfDigits){
  char theNumberString[numberOfDigits + 1];
  int theNumber;
  for (int i = 0; i < numberOfDigits; theNumberString[i++] = Serial.read());
  theNumberString[numberOfDigits] = 0x00;
  theNumber = atoi(theNumberString);
  return theNumber;
}
int pos = 0;    // variable to store the servo position

void setup() {
  Serial.begin(9600)
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
    if (Serial.available()){
    // in steps of 1 degree
    myservo.write(read_num(3));              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}