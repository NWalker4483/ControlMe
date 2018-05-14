int GetMyJrkPosition(byte command)
{
  char response[2];
  myJrk.listen();
  myJrk.write(0xAA);
  myJrk.write(0x0B);//the Device Number is set in the Serial Interface box in the Input tab of your jrk config utility
  myJrk.write(command);
  while (myJrk.available() < 2);//wait for it to become available
  myJrk.readBytes(response,2);
  return word(response[1],response[0]);
}

void GetCurrentPosition()
{
  word feedbackPosition = GetMyJrkPosition(0xA5);
  Serial.print("feedbackPosition: ");
  Serial.println(feedbackPosition);
  word scaledFeedbackPosition = GetMyJrkPosition(0xA7);
  Serial.print("scaledFeedbackPosition: ");
  Serial.println(scaledFeedbackPosition);
}