from flask import Flask, render_template,  Markup, make_response, request, current_app, Response
from flask_socketio import SocketIO, emit
import subprocess, os, datetime, time, json
import time
from threading import Thread
from ignore import de_way
# For Disabling Verbose Mode

import logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

class Engine(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.flow = {}

	def run(self):
		display = ""
		while True:
			time.sleep(0.1)
			#self.flow["Time"] = time.time()
			for i in self.flow:
				flowstr = str(self.flow[i])
				flowstr = flowstr.replace("{","")
				flowstr = flowstr.replace("}","")
				flowstr = flowstr.replace('"',"")
				socketio.emit("flow",
							{"data":[i,flowstr]},
							namespace="/test")	

from Pull_Push import Linear_Actuator
global Actuators
Actuators=dict()
test_environment = True
try:
	import RPi.GPIO as GPIO
	test_environment = False
except ImportError:
	pass
from camera import VideoCamera

async_mode = "threading"
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["TEMPLATES_AUTO_RELOAD"]=True
socketio = SocketIO(app, async_mode=async_mode)

	
secure= False
global Sliders
Sliders=["A","B","C","D"]
Buttname = ["Robot"]
accName= [["Conveyor Belt", "Front Light", "Back Light", "Bright Light"]]
Buttpin = [[7, 17, 27, 22]]

for i in range(len(Sliders)):
	Actuators[Sliders[i]]=Linear_Actuator(lets="ABCD"[i])

if test_environment==False:
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	for i in range(len(Buttpin)):
		GPIO.setup(Buttpin[i], GPIO.OUT, initial=GPIO.LOW)

def accState(roomNumber, accNumber):
	if test_environment==False:	
		if GPIO.input(Buttpin[roomNumber][accNumber]) is 1:
			return "containerOn"
		else:
			return "containerOff"
	else:
		return "containerOff"

@app.route("/")
def main():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %I:%M %p")
	buttons = ""
	sliders = "<table id='Sliders' style='width:100%'; ><tr>"
	for i in range(len(Buttname)):
		buttons = buttons + "<div class='roomtitle'>%s</div>" % (Buttname[i])
		for j in range(len(accName[i])):
			buttonHtmlName = accName[i][j].replace(" ", "<br>")
			buttons = buttons + "<span id='button%d%d'><button class='%s' onclick='toggle(%d,%d)'>%s</button></span>" % (i, j, accState(i,j), i, j, buttonHtmlName)

	for i in range(len(Sliders)):
		sliders = sliders + "<th><p class='roomtitle' id='%s'>%s: </p></th>" % (Sliders[i]+"a",Sliders[i])
	sliders+="</tr>"
	for i in range(len(Sliders)):
		sliders = sliders + "<td><input class='slider' id='%s' orient='vertical' type='range' min='0' max='100' value='50' step='10' onchange=update()/> </td>" % (Sliders[i])
	buttonGrid = Markup(buttons)
	sliderGrid = Markup(sliders+"</table>")

	templateData = {
		"title" : "MSU RMC Control Center",
		"time": timeString,
		"buttons" : buttonGrid,
		"sliders" : sliderGrid
	}
	global thread
	thread = Engine()
	thread.daemon = True
	thread.start()
	return render_template("main.html", **templateData)

@socketio.on("joystick", namespace="/test")    
def steering(message):
		de_way(message["value"][0],message["value"][1])
def dir(x):
	return "F" if x>=50 else "R"
	
@socketio.on("robot", namespace="/test")    
def handle_robot(message):
	##############################################
	###########TESTING CODE TO BE REMOVED#########
	##############################################
	thread.flow[message["motor"]]=message["value"]
	if message["value"]=="GO" and message["motor"]=="shoulder_bottom_right":
		Actuators["A"].move("F",100)
	if message["value"]=="GO" and message["motor"]=="shoulder_top_right":
		Actuators["A"].move("B",100)
	if message["value"]=="STOP":
		Actuators["A"].move("R",0)
	if message["motor"] in Sliders:
		Actuators[message["motor"]].move(dir(int(message["value"])),int(message["value"]))

if test_environment==False:							   
	@app.route("/button/<int:roomNumber>/<int:accNumber>/")
	def toggle(roomNumber, accNumber):
		if len(Buttpin[roomNumber]) != 0:
			state= 1 - GPIO.input(Buttpin[roomNumber][accNumber])
			GPIO.output(Buttpin[roomNumber][accNumber], state)
		else:
			#for handling empty rooms for other rooms
			subprocess.call(["./echo.sh"], shell=True)
		buttonHtmlName = accName[roomNumber][accNumber].replace(" ", "<br>")
		passer="<button class='%s' onclick='toggle(%d,%d)'>%s</button>" % (accState(roomNumber,accNumber), roomNumber, accNumber, buttonHtmlName)
		return passer

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera(kinect=True)),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
	if secure is True:
		#app.run(host="0.0.0.0", port=8000, debug=True, ssl_context=("WebGPIO.cer", "WebGPIO.key"))
		socketio.run(app,host="0.0.0.0",debug=True)
	else:
		#app.run(host="0.0.0.0", port=8000, debug=True)
		socketio.run(app,host="0.0.0.0",debug=False)
