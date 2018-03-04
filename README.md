# MSU Robot Mining Control System 
## Softwares Used 
* Python 3.6
## Necessary Modules
* flask 
* imutils
* flask_socketio
* RPi.GPIO
* getch
* cv2
* pyserial

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
* <del>Switch Jrk Mode from serial to pwm</del>

## Necessary Side Quests
* Slim down modules used/ Remove importing of any unused/noncritical modules
* <del>Review line 33 and 36 in order to implement control of multiple actuators from arduino</del>
* Create better testing modes for both pi and arduino
* Wipe Pi and reinstall backend while logging the setup process 
* Check out[PS2 Controller with jrk21v3](https://arduino.stackexchange.com/questions/17301/linear-actuator-jitters-vibrates-when-getting-pwm-from-arduino-mega-2560-through)
* [Pololu jrk 21v3 Documentation](https://www.pololu.com/docs/pdf/0J38/jrk_motor_controller.pdf) Page 29
* [Implement Differential Steering Algorithms](https://www.impulseadventure.com/elec/robot-differential-steering.html)

## Possible Progression
* Encorporate https://github.com/jeromeetienne/virtualjoystick.js
* * seperate javascript and <del>css</del> into seperate files
* Convert to C++ using [Crow](https://github.com/ipkn/crow)
* Convert Camera module to imutils instead of cv2
* Have backend print ip address on boot.

* <del>Add PC Mode that ignores gpio</del>
* ## [Replicate if Possible]
* * <del>(https://www.youtube.com/watch?v=0Pagiqov-dk)</del>
* * (https://www.youtube.com/watch?v=L5tx64G1ilQ&t=4s)
* * (https://arduino.stackexchange.com/questions/17301/linear-actuator-jitters-vibrates-when-getting-pwm-from-arduino-mega-2560-through)
* * (https://www.arduino.cc/en/Tutorial/Knob)
* * PRIORITY: [Differential drive robot with speed contro](https://www.youtube.com/watch?v=kfT3eoNAM-Q)
* * PRIORITY: Research Gamepad API + Socket.io
 ## Malcolm
 * QuPass Diagnostic Screen
 ## Ambria
 * <del>Control multiple actuators at once from arduino</del>
 * Vanilla Css/Js Vertical Slider
 ## Nile:
 * https://github.com/neogeek/gamepad.js/tree/master

# References/Tutorials
* https://stackoverflow.com/questions/40963401/flask-dynamic-data-update-without-reload-page
* https://github.com/miguelgrinberg/Flask-SocketIO
* https://tutorials.technology/tutorials/61-Create-an-application-with-websockets-and-flask.html
* [Flask Web interface Example](https://forum.poppy-project.org/t/flask-quick-web-interface-for-robots/2217/6)
* https://stackoverflow.com/questions/22259847/application-not-picking-up-css-file-flask-python
* [Motor control setup for pololu jrk21v3 with Arduino UNO R3](https://forum.arduino.cc/index.php?topic=146784.0)
* [CrossDomain](http://flask.pocoo.org/snippets/56/)
* [Multiple Arduino Streams](https://www.arduino.cc/en/Tutorial/TwoPortRece)
* [Jrk21v3 with feedback Arduino](https://forum.pololu.com/t/getting-feedback-from-jrk21v3-with-arduino/8823/6)
* [Gamepad API Demo](https://gamedevelopment.tutsplus.com/tutorials/using-the-html5-gamepad-api-to-add-controller-support-to-browser-games--cms-21345)
