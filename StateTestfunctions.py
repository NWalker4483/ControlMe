'''    
@socketio.on('pad', namespace='/test')    
def handle_pad(message):
    thread.flow['alpha']=message['alpha']
    thread.flow['beta']=message['beta']
    thread.flow['gamma']=message['gamma']
    '''
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
@app.route("/statelist/")
def buttonStates():
	accState=[]
	for i in range(len(Buttpin)):
		accState.append([])
		for j in range(len(Buttpin[i])):
			accState[i].append(1 - GPIO.input(Buttpin[i][j]))
	return json.dumps(accState)

@app.route("/grid/")
@crossdomain(origin='*')
def grid():
	#Safely Aligns all the Buttons
	passer = ''
	for i in range(len(Buttname)):
		passer = passer + "<p class='roomtitle'>%s</p>" % (Buttname[i])
		for j in range(len(accName[i])):
			buttonHtmlName = accName[i][j].replace(" ", "<br>")
			passer = passer + "<span id='button%d%d'><button class='%s' onclick='toggle(%d,%d)'>%s</button></span>" % (i, j, accState(i,j), i, j, buttonHtmlName)
	return passer

@app.route("/setstate/<int:roomNumber>/<int:accNumber>/<int:state>/")
def setstate(roomNumber, accNumber, state):
	if len(Buttpin[roomNumber]) == 1:
		GPIO.output(Buttpin[roomNumber][accNumber], 1 - state)
	#subprocess.call(['./echo.sh'], shell=True)
	else:
		#action for other rooms
		subprocess.call(['./echo.sh'], shell=True)
	return "0"
