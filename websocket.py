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

from threading import Thread
import os
import json
from flask import Flask, render_template, session, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from time import sleep     
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import requests



app = Flask(__name__)
CORS(app, resources={r"/*": {"Access-Control-Allow-Origin": "*"}})
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
# socketio = SocketIO(app, always_connect=True, async_mode=async_mode, engineio_logger=True)
socketio = SocketIO(app, always_connect=True, engineio_logger=True, cors_allowed_origins="*")

thread = None

executor = ThreadPoolExecutor(2)



@app.route('/')
def index():

    return render_template('index.html',data='/SD/')

#@app.route('/url/<parameter>')
#def camera(parameter):

#    print(parameter)
#    return render_template('xxx.html')

@app.route('/sd/', methods = ['POST'])
def process_and_sending_data1():


    jsondata = request.get_json()
    data = json.loads(jsondata)
    
    #executor.submit(socketio.emit('data_XXX',json.dumps({"key":data[0]['key']}),  broadcast = True))
    
    #contoh bila ada kiriman image ke web page
    executor.submit(socketio.emit('socialDistancing',json.dumps({"img":data[0]['img']}),  broadcast = True))

    result = {'response': True}
    return json.dumps(result)

@app.route('/eye/', methods = ['POST'])
def process_and_sending_data2():


    jsondata = request.get_json()
    data = json.loads(jsondata)
    
    #executor.submit(socketio.emit('data_XXX',json.dumps({"key":data[0]['key']}),  broadcast = True))
    
    #contoh bila ada kiriman image ke web page
    executor.submit(socketio.emit('eye',json.dumps({"img":data[0]['img']}),  broadcast = True))

    result = {'response': True}
    return json.dumps(result)

    #print(result)



@socketio.on('dataXXX')
def handle_data(data):


    executor.submit(socketio.emit('data_for_module',json.dumps({"key":"value"}), broadcast = True, include_self=False))



@socketio.on('connect')
def connected():
    print('connected from client')


@socketio.on('disconnect')
def disconnect():
    print('disconnect')

if __name__ == '__main__':

    print("Websocket Starting...")
    socketio.run(app, debug=True, host='0.0.0.0', port=3000)

