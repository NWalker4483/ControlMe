#from datetime import timedelta
#from functools import update_wrapper
from flask import Flask, render_template,  Markup, make_response, request, current_app, Response
from flask_socketio import SocketIO, emit
import subprocess, os, datetime, time, json
import time
from threading import Thread
test_environment = True
try:
	import RPi.GPIO as GPIO
	test_environment = False
except ImportError:
	pass
from camera import VideoCamera

async_mode = 'threading'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD']=True
socketio = SocketIO(app, async_mode=async_mode)
thread = None

class Engine(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.flow = {}

	def run(self):
		display = ''
		while True:
			time.sleep(0.1)
			#self.flow["Time"] = time.time()
			for i in self.flow:
				flowstr = str(self.flow[i])
				flowstr = flowstr.replace('{','')
				flowstr = flowstr.replace('}','')
				flowstr = flowstr.replace("'",'')
				socketio.emit('flow',
							{'data':[i,flowstr]},
							namespace='/test')
				
secure= True
Sliders=['Speed','Arm']
slides=[[18],[]]
Buttname = ['Robot', 'Server Room']
accName= [['Conveyor Belt', 'Front Light', 'Back Light', 'Bright Light'], ['The Brain']]
Buttpin = [[7, 17, 27, 22],[27]]
if test_environment==False:
	from pisces import ESC
	from Pull_Push import Linear_Actuator
	global M1 , M2
	M1=ESC(18)
	M2=Linear_Actuator()
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	for i in range(len(Buttpin)):
		GPIO.setup(Buttpin[i], GPIO.OUT, initial=GPIO.LOW)

def accState(roomNumber, accNumber):
	if test_environment==False:	
		if GPIO.input(Buttpin[roomNumber][accNumber]) is 1:
			return 'containerOn'
		else:
			return 'containerOff'
	else:
		return 'containerOff'

@app.route("/")
def main():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %I:%M %p")
	buttons = ''
	sliders = ''
	for i in range(len(Buttname)):
		buttons = buttons + "<p class='roomtitle'>%s</p>" % (Buttname[i])
		for j in range(len(accName[i])):
			buttonHtmlName = accName[i][j].replace(" ", "<br>")
			buttons = buttons + "<span id='button%d%d'><button class='%s' onclick='toggle(%d,%d)'>%s</button></span>" % (i, j, accState(i,j), i, j, buttonHtmlName)
	
	for i in range(len(Sliders)):
		sliders = sliders + "<div><p class='roomtitle' id='%s'>%s: </p>" % (Sliders[i]+'a',Sliders[i])
		sliders = sliders + "	<input class='slider' id='%s' orient='vertical' type='range' min='0' max='100' value='50' step='10'/> <br></div>" % (Sliders[i])
	buttonGrid = Markup(buttons)
	sliderGrid = Markup(sliders)
	templateData = {
		'title' : 'MSU RMC Control Center',
		'time': timeString,
		'buttons' : buttonGrid,
		'sliders' : sliderGrid
	}
	global thread
	#if thread is None:
	thread = Engine()
	thread.daemon = True
	thread.start()
	return render_template('main.html', **templateData)

@socketio.on('robot', namespace='/test')    
def handle_robot(message):
	print('Signal Recieved')
	thread.flow[message['motor']]=message['value']
	if test_environment==False:
		if message['motor']=='Speed':
			M1.update(int(message['value']))
		if message['motor']=='Arm':
			M2.move(int(message['value']))
	
if test_environment==False:							   
	@app.route("/button/<int:roomNumber>/<int:accNumber>/")
	def toggle(roomNumber, accNumber):
		if len(Buttpin[roomNumber]) != 0:
			state= 1 - GPIO.input(Buttpin[roomNumber][accNumber])
			GPIO.output(Buttpin[roomNumber][accNumber], state)
		else:
			#for handling empty rooms for other rooms
			subprocess.call(['./echo.sh'], shell=True)
		buttonHtmlName = accName[roomNumber][accNumber].replace(" ", "<br>")
		passer="<button class='%s' onclick='toggle(%d,%d)'>%s</button>" % (accState(roomNumber,accNumber), roomNumber, accNumber, buttonHtmlName)
		return passer

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
	if secure is True:
		#app.run(host='0.0.0.0', port=8000, debug=True, ssl_context=('WebGPIO.cer', 'WebGPIO.key'))
		socketio.run(app,host='0.0.0.0',debug=True)
	else:
		#app.run(host='0.0.0.0', port=8000, debug=True)
		socketio.run(app,host='0.0.0.0',debug=False)
