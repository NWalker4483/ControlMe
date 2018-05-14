#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = 'threading'
from flask import Flask, render_template, redirect, Markup, make_response, request, current_app, Response

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

import time
from threading import Thread
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
import csv

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
            time.sleep(0.05)
            self.flow["t"] = time.time()
            flowstr = str(self.flow)
            flowstr = flowstr.replace(',','<br>')
            flowstr = flowstr.replace('{','')
            flowstr = flowstr.replace('}','')
            socketio.emit('flow',
                          {'data': flowstr},
                          namespace='/test')
            
@app.route('/')

def index():
    global thread
    if thread is None:
        thread = Engine()
        thread.daemon = True
        thread.start()
    return render_template('index.html')

@socketio.on('robot', namespace='/test')    
def handle_robot(message):
    thread.flow[message['motor']]=message['value']
def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
from camera import VideoCamera

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')    
@socketio.on('pad', namespace='/test')    
def handle_pad(message):
    thread.flow['alpha']=message['alpha']
    thread.flow['beta']=message['beta']
    thread.flow['gamma']=message['gamma']


@app.route('/tel')
def tel():
    frame_name = "dogs"
    return render_template("tel.html", fname=frame_name)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)