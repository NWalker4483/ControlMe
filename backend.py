from datetime import timedelta
from functools import update_wrapper
from flask import Flask, render_template,  Markup, make_response, request, current_app, Response
from flask_socketio import SocketIO, emit
#import RPi.GPIO as GPIO
import GPIO
import subprocess, os, datetime, time, json
#from pisces import ESC
import time
from threading import Thread

import random
from pisces import ESC
from camera import VideoCamera
'''
if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()
	'''



async_mode = 'threading'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
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
            flowstr = str(self.flow)
            flowstr = flowstr.replace(',','<br>')
            flowstr = flowstr.replace('{','')
            flowstr = flowstr.replace('}','')
            flowstr = flowstr.replace("'",'')
            socketio.emit('flow',
                          {'data': flowstr},
                          namespace='/test')
secure= False
Sliders=['Speed','Doggos']
slides=[[17],[]]
Buttname = ['Robot', 'Server Room']
accName= [['Conveyor Belt', 'Front Light', 'Back Light', 'Bright Light'], ['The Brain']]
Buttpin = [[7, 17, 27, 22],[27]]


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(len(Buttpin)):
	GPIO.setup(Buttpin[i], GPIO.OUT, initial=GPIO.LOW)

def accState(roomNumber, accNumber):
	if GPIO.input(Buttpin[roomNumber][accNumber]) is 1:
		return 'containerOn'
	else:
		return 'containerOff'

def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
	if methods is not None:
		methods = ', '.join(sorted(x.upper() for x in methods))
	if headers is not None and not isinstance(headers, list):
		headers = ', '.join(x.upper() for x in headers)
	if not isinstance(origin, list):
		origin = ', '.join(origin)
	if isinstance(max_age, timedelta):
		max_age = max_age.total_seconds()
	
	def get_methods():
		if methods is not None:
			return methods
		
		options_resp = current_app.make_default_options_response()
		return options_resp.headers['allow']
	
	def decorator(f):
		def wrapped_function(*args, **kwargs):
			if automatic_options and request.method == 'OPTIONS':
				resp = current_app.make_default_options_response()
			else:
				resp = make_response(f(*args, **kwargs))
			if not attach_to_all and request.method != 'OPTIONS':
				return resp
			
			h = resp.headers
			h['Access-Control-Allow-Origin'] = origin
			h['Access-Control-Allow-Methods'] = get_methods()
			h['Access-Control-Max-Age'] = str(max_age)
			h['Access-Control-Allow-Credentials'] = 'true'
			h['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept, Authorization"
			if headers is not None:
				h['Access-Control-Allow-Headers'] = headers
			return resp
						
		f.provide_automatic_options = False
		return update_wrapper(wrapped_function, f)
	return decorator


@app.route("/")
def main():
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d %I:%M %p")
	passer = ''
	for i in range(len(Buttname)):
		passer = passer + "<p class='roomtitle'>%s</p>" % (Buttname[i])
		for j in range(len(accName[i])):
			buttonHtmlName = accName[i][j].replace(" ", "<br>")
			passer = passer + "<span id='button%d%d'><button class='%s' onclick='toggle(%d,%d)'>%s</button></span>" % (i, j, accState(i,j), i, j, buttonHtmlName)
	for i in range(len(Sliders)):
		passer = passer + "<div><p class='roomtitle' id='%s'></p>" % (Sliders[i]+'a')
		passer = passer + "	<input class='slider' id='%s' type='range' min='0' max='1' value='0.5' step='0.01'/> <br></div>" % (Sliders[i])
	buttonGrid = Markup(passer)
	templateData = {
		'title' : 'MSU RMC Control Center',
		'time': timeString,
		'buttons' : buttonGrid,
	}
	global thread
	global Tert
	Tert=ESC(7)
	#if thread is None:
	thread = Engine()
	thread.daemon = True
	thread.start()
	return render_template('main.html', **templateData)

@socketio.on('robot', namespace='/test')    
def handle_robot(message):
	thread.flow[message['motor']]=message['value']
	if message['motor']=='Speed':
		Tert.update(100*float(message['value']))

							   
@app.route("/button/<int:roomNumber>/<int:accNumber>/")
@crossdomain(origin='*')
def toggle(roomNumber, accNumber):
	if len(Buttpin[roomNumber]) != 0:
		state= 1 - GPIO.input(Buttpin[roomNumber][accNumber])
		GPIO.output(Buttpin[roomNumber][accNumber], state)
		#subprocess.call(['./echo.sh'], shell=True)
		pass
	else:
		#for handling empty rooms for other rooms
		subprocess.call(['./echo.sh'], shell=True)
	#print(roomNumber, accNumber)
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
