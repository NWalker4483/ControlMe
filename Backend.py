##MODULES
from flask import Flask, render_template,  Markup, Response,request,flash, jsonify
from flask_socketio import SocketIO, emit
import os, datetime, time


from Engine import Engine
from ignore import de_way #for joysticking
from camera import VideoCamera
import cv2
from Pull_Push import Linear_Actuator
# For Disabling Verbose Mode
#SETTINGS
test_environment = True
Kinect=True
secure=True
async_mode = "threading"
Listening=False
Verbose=True

if not Verbose:
	import logging
	log = logging.getLogger("werkzeug")
	log.setLevel(logging.ERROR)

if Listening:
	from chatterbot import ChatBot
	from chatterbot.trainers import ChatterBotCorpusTrainer
	english_bot = ChatBot("zee")
	english_bot.set_trainer(ChatterBotCorpusTrainer)
	english_bot.train("chatterbot.corpus.english")
	english_bot.train('chatterbot.corpus.english.greetings')
	english_bot.train('chatterbot.corpus.english.conversations')


def make_controls(a,b):
	controls=" gamepad.setCustomMapping('keyboard', {'button_1': 32,'start': 27,'d_pad_up': [38, 87],'d_pad_down': [40, 83],'d_pad_left': [37, 65],'d_pad_right': [39, 68]});"
	for i in zip(a,b):
		controls+="gamepad.on('press', '{0}', e => {{ socket.emit('robot', {{motor: '{1}' ,value:'GO'}});}});".format(i[0],i[1])
		controls+="gamepad.on('release', '{0}', e => {{socket.emit('robot', {{motor: '{1}' ,value:'STOP'}});}});".format(i[0],i[1])
	return controls


global Actuators
Actuators=dict()



app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["TEMPLATES_AUTO_RELOAD"]=True
socketio = SocketIO(app, async_mode=async_mode)

	

global Sliders

Sliders=["A","B"]
Buttname = ["shoulder_bottom_right",'shoulder_top_right']
accName= [["Conveyor Belt", "Front Light", "Back Light", "Bright Light"]]
#Buttpin = [[7, 17, 27, 22]]

for i in range(len(Sliders)):
	if i<4:
		Actuators[Sliders[i]]=Linear_Actuator(lets="0123"[i])

@app.route("/")
def main():
	global thread
	thread = Engine(socketio)
	thread.daemon = True
	thread.start()
	templateData = {
		"title" : "MSU RMC Control Center",
		"controls": make_controls(Buttname,Sliders)
	}
	return render_template("main.html",**templateData)

@socketio.on("joystick", namespace="/test")    
def steering(message):
	print(message['motor'])
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
		frame = camera.get_frame(depth=True)
		frame=cv2.imencode('.jpg',frame)[1].tobytes()
		yield (b"--frame\r\n"
				b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera(Kinect)),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
if Listening:
	@app.route("/ask", methods=['POST'])
	def ask():
		message = (request.form['messageText'])

		while True:
			if message == "":
				continue
			else:
				com=message.split()
				print(message)
				bot_response = str(english_bot.get_response(message))
				# print bot_response
				return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
	if secure is True:
		#app.run(host="0.0.0.0", port=8000, debug=True, ssl_context=("WebGPIO.cer", "WebGPIO.key"))
		socketio.run(app,host="0.0.0.0",debug=True)
	else:
		#app.run(host="0.0.0.0", port=8000, debug=True)
		socketio.run(app,host="0.0.0.0",debug=False)
