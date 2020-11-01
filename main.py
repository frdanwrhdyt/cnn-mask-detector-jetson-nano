from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import tensorflow as tf
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os
import base64
import json
import requests
from playsound import playsound
from time import sleep
# import firebase_admin
# from firebase_admin import db, credentials
from threading import Thread

class SocialDistancing:
    def __init__ (self):
        self.websocketServer = 'http://192.168.10.34:3000'
        
        print("[INFO] loading face detector model...")
        prototxtPath = os.path.sep.join(['face_detector', "deploy.prototxt"])
        weightsPath = os.path.sep.join(['face_detector',"res10_300x300_ssd_iter_140000.caffemodel"])
        self.faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

        print("[INFO] loading face mask detector model...")
        self.maskNet = load_model('mask_detector2.model')

        print("[INFO] starting video stream...")
        self.vs = VideoStream(src=0).start()

    def play_song_menjauh(self):
        playsound('music/menjauh.wav')

    def play_song_masker(self):
        playsound('music/masker.wav')

    def detect_and_predict_mask(self, frame, faceNet, maskNet):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0))
        faceNet.setInput(blob)
        detections = faceNet.forward()

        faces = []
        locs = []
        preds = []
        for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    (startX, startY) = (max(0, startX), max(0, startY))
                    (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

                    face = frame[startY:endY, startX:endX]
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                    face = cv2.resize(face, (100, 100))
                    face = img_to_array(face)
                    face = preprocess_input(face)

                    faces.append(face)
                    locs.append((startX, startY, endX, endY))
        if len(faces) > 0:
            faces = np.array(faces, dtype="float32")
            preds = maskNet.predict(faces, batch_size=32)
        return (locs, preds)
    def delay_song(self, i):
        sleep(i)    
    def processing_and_sending(self):
        # cred = credentials.Certificate('certificate/btp-imageprocessing-firebase-adminsdk-fo73c-90fb7a6519.json')
        # firebase_admin.initialize_app(cred,{
        #     'databaseURL' : 'https://btp-imageprocessing.firebaseio.com/',
        # })
        # ref = db.reference ('/')
        alarm_on = False
        time.sleep(2)
        width_frame = 360
        treshold = 100
        faceNet = self.faceNet
        maskNet = self.maskNet
        while True:
            file1 = open('sound.txt', 'w')
            file1.write("1")
            file1.close()
            d = 0
            i = 0
            frame = self.vs.read()
            frame = imutils.resize(frame, width=width_frame)
            frame1 = frame.copy()
            (locs, preds) = self.detect_and_predict_mask(frame, faceNet, maskNet)
            boxs = []
            x1 = []
            x2 = []
            y1 = []
            y2 = []
            mid_x = []
            for (box, pred) in zip(locs, preds):
                boxs.append(box)
                print(boxs)
                if len(boxs)>1:
                    n = len(boxs)
                    for i in range (0, n):
                        x1.append(boxs[i][0])
                        y1.append(boxs[i][1])
                        x2.append(boxs[i][2])
                        y2.append(boxs[i][3])
                        mid_x.append((boxs[i][0])-(boxs[i][2]))
                    for j in range (0, len(x1)):
                        for i in range (0, len(x1)-j-1):
                            if x2[i]-x1[i]<x2[i+1]-x1[i+1]:
                                x1[i], x2[i], x1[i+1], x2[i+1] = x1[i+1], x2[i+1], x1[i], x2[i]
                    for j in range (1, len(x1)):
                        dis = (x2[j-1]-x1[j-1])/2
                        dis = dis - ((x2[j]-x1[j])/2)
                        dis = dis + ((x1[j-1]*x2[j-1])/(x2[j]-x1[j]))
                        dis = dis / width_frame
                        dis = 1-dis
                        dis = dis * treshold
                        # dis = -dis
                    if dis < 0:
                        dis = -dis
                    
                    d = dis
                    print(dis)
                    # return dis
                (startX, startY, endX, endY) = box
                (mask, withoutMask) = pred
                #t = Thread(target = self.play_song_masker)
                # t.deamon = True
                #r = Thread(target = self.play_song_menjauh)
                # r.deamon = True
                # file1 = open("sound.txt","w") 
                label = "Mask" if mask > withoutMask else "No Mask"
                color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
                label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
                cv2.putText(frame, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                if d > 5 and d < 200:
                    # t.start()
                # elif t.start():      #ga pake masker
                    # t.join()
                    file1 = open('sound.txt', 'w')
                    file1.write("2")
                    file1.close()
                elif  withoutMask > mask :
                        # play(self.song)
                    for j in range (1, len(x1)):
                        cv2.line(frame, (mid_x[j-1], y1[j-1]), (mid_x[j], y1[j]), (255, 0, 0), 1)
                        cv2.putText(frame, 'Too Close', (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                    file1 = open('sound.txt', 'w')
                    file1.write("0")
                    file1.close()
                # else:
                #     if frame is not None:
                        

                # else:
            # alarm_on = True
            img_to_base64_1 = base64.b64encode(cv2.imencode('.jpg', frame)[1]).decode()
            conv1 = [{'img' : img_to_base64_1}]

            img_to_base64_2 = base64.b64encode(cv2.imencode('.jpg', frame1)[1]).decode()
            conv2 = [{'img' : img_to_base64_2}]
            
            sendData1 = json.dumps(conv1)
            requests.post(self.websocketServer+"/sd/", json=sendData1).json()

            sendData2 = json.dumps(conv2)
            requests.post(self.websocketServer+"/eye/", json=sendData2).json()

            # return dis

if __name__ == '__main__':
    SocialDistancing().processing_and_sending()
