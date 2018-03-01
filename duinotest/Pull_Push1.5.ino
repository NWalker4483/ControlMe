/*
 Controlling a servo position using a potentiometer (variable resistor)
 by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>

 modified on 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Knob
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int potpin = 0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin
int myTarget = 0; // target position, 0-4095 is the range of the JRK21V3 controller. 

//stuff used for input from pc
char buffer[5] ;
int pointer = 0;
byte inByte = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Initialized");
  Serial.flush();// Give reader a chance to see the output.

  Serial.println("Enter '#' and 4 digit position level (#0000-#4095)");
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  if (Serial.available() >0) {
   // read the incoming byte:
   inByte = Serial.read();
   delay(10);
   
   // If the marker's found, next 4 characters are the position
    if (inByte == '#') {
      while (pointer < 3) { // accumulate 4 chars
        buffer[pointer] = Serial.read(); // store in the buffer
        pointer++; // move the pointer forward by 1
      }
      Serial.flush();
      //translating into an int
      myTarget=(buffer[0]-48)*1000+(buffer[1]-48)*100+(buffer[2]-48)*10;
      pointer =0;
    }
   //makes sure the target is within the bounds
   if (myTarget < 0){
      myTarget = 0;
      }
   else if (myTarget > 180){
      myTarget=180;
      }
        myservo.write(myTarget);                  // sets the servo position according to the scaled value
  delay(15);

  }
            // reads the value of the potentiometer (value between 0 and 1023)     // scale it to use it with the servo (value between 0 and 180)
                           // waits for the servo to get there
}