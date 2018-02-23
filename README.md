# MSU Robot Mining Control System 
## Softwares Used 
* Python 3.6
## Necessary Modules
* flask 
* imutils
* flask_socketio
* RPi.GPIO
* getch

## Steps of progression
* <del>Install Raspbian OS on Pi</del>
* <del>Setup & Test [WebGPIO](https://github.com/ThisIsQasim/WebGPIO)</del>
* Combine [GamePad API Demo](https://github.com/luser/gamepadtest) with [WebGPIO](https://github.com/ThisIsQasim/WebGPIO)
* * <del>Ensure that analog data can be read & utilized by [WebGPIO]</del>(https://github.com/ThisIsQasim/WebGPIO)
* <del> Setup Video Stream from webcam </del>
* Control ___ with the webpage and or gamepad input:
* * <del>LED</del>
* * <del>ESC</del> 
* * Mosfet 
* <del>[Signal Arduino with Pi](https://maker.pro/education/how-to-connect-and-interface-a-raspberry-pi-with-an-arduino) </del>
* <del>Switch control to an Arduino [Roboteq](https://github.com/kippandrew/Arduino-RobotEQ)</del>
* <del>[Control Linear Actuator](https://www.marginallyclever.com/2015/07/how-to-control-a-linear-actuator-with-an-arduino/) with Arduino</del>
* <del>Connect webcam to servo </del> which is controlled via gamepad
* Test the bandwidth utilized by the stream
* seperate javascript and <del>css</del> into seperate files
## Necessary Side Quests
* Slim down modules used/ Remove importing of any unused/noncritical modules
* Review line 33 and 36 in order to implement control of multiple actuators from arduino
* Wipe Pi and reinstall backend while logging the setup process 
## Possible Progression
* Convert to C++ using [Crow](https://github.com/ipkn/crow)
* Convert Camera module to imutils instead of cv2
# References/Tutorials
* https://stackoverflow.com/questions/40963401/flask-dynamic-data-update-without-reload-page
* https://github.com/miguelgrinberg/Flask-SocketIO
* https://tutorials.technology/tutorials/61-Create-an-application-with-websockets-and-flask.html
* [Flask Web interface Example](https://forum.poppy-project.org/t/flask-quick-web-interface-for-robots/2217/6)
* https://stackoverflow.com/questions/22259847/application-not-picking-up-css-file-flask-python
* [Motor control setup for pololu jrk21v3 with Arduino UNO R3](https://forum.arduino.cc/index.php?topic=146784.0)
* [CrossDomain](http://flask.pocoo.org/snippets/56/)
* [Multiple Arduino Streams](https://www.arduino.cc/en/Tutorial/TwoPortRece)
