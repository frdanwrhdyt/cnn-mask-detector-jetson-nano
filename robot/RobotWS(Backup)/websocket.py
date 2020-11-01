async_mode = ''

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

if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
from threading import Thread
import os
import cv2
import base64
import json
from flask import Flask, render_template, session, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from threading import Event # Needed for the  wait() method
from time import sleep     
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import requests



app = Flask(__name__)
CORS(app, resources={r"/*": {"Access-Control-Allow-Origin": "*"}})
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# socketio = SocketIO(app, always_connect=True, async_mode=async_mode, engineio_logger=True)
socketio = SocketIO(app, always_connect=True, engineio_logger=True)

thread = None

executor = ThreadPoolExecutor(2)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/sendDataRobot/', methods = ['POST'])
def get_data():


    jsondata = request.get_json()
    data = json.loads(jsondata)
    executor.submit(socketio.emit('data_info_robot',json.dumps({"sensor":data[0]['sensor'],
    "batre":data[0]['batre'],"led":data[0]['led'],
    "emergency":data[0]['emergency'] }),  room = 'robot'))
       
    result = {'response': True}
    return json.dumps(result)

@app.route('/sendDataRobotSensor/', methods = ['POST'])
def get_data_sensor():
    jsondata = request.get_json()
    data = json.loads(jsondata)
    executor.submit(socketio.emit('data_info_robot',json.dumps({"sensor":data[0]['sensor'], "batre":data[0]['batre']})
    , room = 'robot'))
    
    result = {'response': True}
    return json.dumps(result)


@socketio.on('join_group')
def handle_event(data):

    room = data['channel']
    join_room(room)

@socketio.on('control')
def handle_event(control):
    executor.submit(socketio.emit('data_for_robot',json.dumps({"control":control}),room='robot', include_self=False))


@socketio.on('connect')
def connected():
    print('connected from client')


@socketio.on('disconnect')
def disconnect():
    print('disconnect')

if __name__ == '__main__':

    print("Websocket Starting...")
    socketio.run(app, debug=True, host='192.168.10.111')
