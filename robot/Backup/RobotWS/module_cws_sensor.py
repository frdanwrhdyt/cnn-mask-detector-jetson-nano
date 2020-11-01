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


class Data_Sender_Sensor:

	def __init__(self):


		self.websocketServer = 'http://192.168.10.111:5000'

		self.ser = serial.Serial('/dev/ttyUSB_usonic', timeout=1)


		if self.ser.is_open:
		    self.ser.close()
		self.ser.open()
		self.send_loop_sensor()

	def send_loop_sensor(self):

		while True:
			res = self.ser.readline()
			res = res.decode('utf-8')
			res = res.lstrip('#')
			res = res.strip('~\r\n')
			if res != '':
				res = res.split(',')
				sensor = res[0:8]
				#print(sensor)
				batre = res[8:11]
				#print(batre)
				conv = [{ 'sensor':sensor , 'batre': batre}]
				s = json.dumps(conv)
				print(s)
				j = requests.post(self.websocketServer+"/sendDataRobotSensor/", json=s).json()




if __name__ == '__main__':

	ds = Data_Sender_Sensor()






