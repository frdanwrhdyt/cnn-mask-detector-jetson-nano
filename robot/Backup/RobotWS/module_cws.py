import numpy as np
import argparse
import imutils
import time
import cv2
import os
import datetime
import uuid
import base64
import requests
import json
import socketio
import serial

welcome = 'Starting...'
code_maju = '#1,1,1~'
code_stop_maju = '#1,1,0~'
code_mundur = '#1,2,1~'
code_stop_mundur ='#1,2,0~'
code_kiri ='#1,4,1~'
code_stop_kiri ='#1,4,0~'
code_kanan ='#1,3,1~'
code_stop_kanan ='#1,3,0~'
code_naik ='#1,5,1~'
code_stop_naik ='#1,5,0~'
code_turun ='#1,6,1~'
code_stop_turun ='#1,5,0~'
code_prefix_atur_kecepatan ='#1,7,'
code_request_data ='#1,8,1~'
code_start ='#1,9,1~'
code_running_text ='#1,10,1~'
code_emergency_button ='#1,11,1~'
code_warning_light ='#1,12,1~'

class Data_Sender:

	def __init__(self):

		print(welcome)

		self.websocketServer = 'http://192.168.10.111:5000'

		self.ser = serial.Serial('/dev/ttyUSB_robocontrol', 9600 ,timeout=1)


		if self.ser.is_open:
		    self.ser.close()

		self.ser.open()

		self.activate_client_websocket()
		self.process_and_sending_data()


	def activate_client_websocket(self):

		sio = socketio.Client()


		@sio.event
		def connect():
		    sio.emit('join_group', {'channel': 'robot'});

		@sio.event
		def connect_error():
		    print("The connection failed!")

		@sio.event
		def disconnect():
		    print("I'm disconnected!")

		@sio.on('data_for_robot')
		def on_message(data):
			command_control = json.loads(data)
			control =  command_control['control']

			print(control)

			if control == 'maju':
				self.ser.write(bytes(code_maju,encoding='utf-8'))

			elif control == 'stop maju':
				self.ser.write(bytes(code_stop_maju,encoding='utf-8'))

			elif control == 'mundur':
				self.ser.write(bytes(code_mundur,encoding='utf-8'))

			elif control == 'stop mundur':
				self.ser.write(bytes(code_stop_mundur,encoding='utf-8'))

			elif control == 'kiri':
				self.ser.write(bytes(code_kiri,encoding='utf-8'))

			elif control == 'stop kiri':
				self.ser.write(bytes(code_stop_kiri,encoding='utf-8'))

			elif control == 'kanan':
				self.ser.write(bytes(code_kanan,encoding='utf-8'))

			elif control == 'stop kanan':
				self.ser.write(bytes(code_stop_kanan,encoding='utf-8'))

			elif control == 'naik':
				self.ser.write(bytes(code_naik,encoding='utf-8'))

			elif control == 'stop naik':
				self.ser.write(bytes(code_stop_naik,encoding='utf-8'))

			elif control == 'turun':
				self.ser.write(bytes(code_turun,encoding='utf-8'))

			elif control == 'stop turun':
				self.ser.write(bytes(code_stop_turun,encoding='utf-8'))

			elif control == 'request data':
				self.ser.write(bytes(code_request_data,encoding='utf-8'))

				res = self.ser.readline()
				res = res.decode('utf-8')

				print(res)

				sensor = res[1:16]
				print('Sensor: '+sensor)

				batre = res[17:22]
				print('Batre: '+batre)

				led = res[23]
				print('Led: '+led)

				emergency = res[25]
				print('Emergency: '+emergency)

				conv = [{ 'sensor':sensor, "batre":batre, "led": led, "emergency": emergency}]

				s = json.dumps(conv)

				res = requests.post(self.websocketServer+"/sendDataRobot/", json=s).json()

			elif '->' in control:
				self.ser.write(bytes(code_prefix_atur_kecepatan+control[2:],encoding='utf-8'))

			elif control == 'emrbut':
				self.ser.write(bytes(code_emergency_button,encoding='utf-8'))

			elif control == 'strt':
				self.ser.write(bytes(code_start,encoding='utf-8'))
			
			elif control == 'WL':
				self.ser.write(bytes(code_warning_light,encoding='utf-8'))
			
			elif control == 'RT':
				self.ser.write(bytes(code_running_text,encoding='utf-8'))

		sio.connect(self.websocketServer)


	def process_and_sending_data(self):
		pass


if __name__ == '__main__':


	ds = Data_Sender()
