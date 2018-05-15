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
secure=False
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



def make_controls(a):
	controls=" gamepad.setCustomMapping('keyboard', {'button_1': 32,'start': 27,'d_pad_up': [38, 87],'d_pad_down': [40, 83],'d_pad_left': [37, 65],'d_pad_right': [39, 68]});"
	for motor in a:
		controls+="gamepad.on('press', '{0}', e => {{ socket.emit('robot', {{motor: '{1}' ,value:[{2},{3}]}});}});".format(a[motor][1],motor,a[motor][4][0],a[motor][3][0])
		controls+="gamepad.on('release', '{0}', e => {{socket.emit('robot', {{motor: '{1}' ,value:[0,{2}]}});}});".format(a[motor][1],motor,a[motor][3][2])
		controls+="gamepad.on('press', '{0}', e => {{ socket.emit('robot', {{motor: '{1}' ,value:[{2},{3}]}});}});".format(a[motor][2],motor,a[motor][4][1],a[motor][3][1])
		controls+="gamepad.on('release', '{0}', e => {{socket.emit('robot', {{motor: '{1}' ,value:[0,{2}]}});}});".format(a[motor][2],motor,a[motor][3][2])
	
	return controls


global Motors
Motors=Linear_Actuator()



app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["TEMPLATES_AUTO_RELOAD"]=True
socketio = SocketIO(app, async_mode=async_mode)


#Name : inByte Button 1, Button 2, Available dirs , speeds
Motor_Names={"Lift Arm":(2,"shoulder_bottom_left",'shoulder_top_leftt',['F','B','R'],[100,100]),\
             "Scoop":(3,"shoulder_bottom_right",'shoulder_top_right',['F','F','R'],[100,50]),\
			  "Dump_Lower":(4,"button_1","button_3",['F','B','R'],[100,100]),\
			   "Dump_Upper":(5,"button_2","button_4",['F','B','R'],[100,100]),\
			   "Right":(6,"d_pad_right","PlaceHolder",['F','N','R'],[100,100]),\
			   "Left":(7,"d_pad_left","PlaceHolder",['F','N','R'],[100,100])
			   }

@app.route("/")
def main():
	global thread
	thread = Engine(socketio)
	thread.daemon = True
	thread.start()
	templateData = {
		"title" : "MSU RMC Control Center",
		"controls": make_controls(Motor_Names)
	}
	return render_template("main.html",**templateData)

@socketio.on("joystick", namespace="/test")    
def steering(message):
	print(message['motor'])
	_right,_left=de_way(message["value"][0],message["value"][1])
	Motors.drive(_right,_left)
def dir(x):
	return "F" if x>=50 else "R"

@socketio.on("robot", namespace="/test")    
def handle_robot(message):
	##############################################
	###########TESTING CODE TO BE REMOVED#########
	##############################################
	###########Button    motor    dir    #########
	thread.flow[message["motor"]]=message["value"]
	if message["motor"] in Motor_Names:
		Motors.move(Motor_Names[message["motor"]][0],message["value"][0],message["value"][1])

def gen(camera):
    while True:
	    frame = camera.get_frame()
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
