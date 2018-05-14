String data="Hello From Arduino!";
int read_num(int numberOfDigits){
  char theNumberString[numberOfDigits + 1];
  int theNumber;
  for (int i = 0; i < numberOfDigits; theNumberString[i++] = Serial.read());
  theNumberString[numberOfDigits] = 0x00;
  theNumber = atoi(theNumberString);
  return theNumber;
void setup() {
// put your setup code here, to run once:
Serial.begin(9600);

}

void loop() {if (Serial.available())
{
// put your main code here, to run repeatedly:
Serial.println(data);//data that is being Sent
it=read_num(3);
at=read_num(2);
Serial.println(it);
Serial.println(at);
}}

