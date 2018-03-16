from flask import Flask, render_template,  Markup, Response
from flask_socketio import SocketIO, emit
import subprocess, os, datetime, time
import time
from threading import Thread
from ignore import de_way
# For Disabling Verbose Mode
'''
import logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
'''
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
show_buttons=False
global Sliders
Sliders=["A","B","C","D"]
Buttname = ["Robot"]
accName= [["Conveyor Belt", "Front Light", "Back Light", "Bright Light"]]
Buttpin = [[7, 17, 27, 22]]

for i in range(len(Sliders)):
	if i<4:
		Actuators[Sliders[i]]=Linear_Actuator(lets="1234"[i])

@app.route("/")
def main():
	global thread
	thread = Engine()
	thread.daemon = True
	thread.start()
	return render_template("main.html")

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
	###########Button    motor    dir    #########
	thread.flow[message["motor"]]=message["value"]
	if message["value"]=="GO" and message["motor"]=="shoulder_bottom_right":
		Actuators["1"].move("F",100)
	if message["value"]=="GO" and message["motor"]=="shoulder_top_right":
		Actuators["1"].move("B",100)
	if message["value"]=="STOP":
		Actuators["1"].move("R",0)
	if message["motor"] in Sliders:
		Actuators[message["motor"]].move(dir(int(message["value"])),int(message["value"]))

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
	if secure is True:
		#app.run(host="0.0.0.0", port=8000, debug=True, ssl_context=("WebGPIO.cer", "WebGPIO.key"))
		socketio.run(app,host="0.0.0.0",debug=True)
	else:
		#app.run(host="0.0.0.0", port=8000, debug=True)
		socketio.run(app,host="0.0.0.0",debug=False)
