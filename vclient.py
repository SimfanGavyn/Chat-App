
from socket import *
import threading
import cv2
import sys
import struct
import pickle
import time
import zlib
import numpy as np

class Video_Client():
    def __init__(self ,ip, port, level, version):
        self.ADDR = (ip, port)
        if level <= 3:
            self.interval = level
        else:
        	self.interval = 3
        self.fx = 1 / (self.interval + 1)
        if self.fx < 0.3:
            self.fx = 0.3
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)
        self.cap = cv2.VideoCapture(0)
    def __del__(self) :
        self.sock.close()
        self.cap.release()
    def run(self):
        print("VEDIO client starts...")
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                time.sleep(3)
                continue
        print("VEDIO client connected...")
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            sframe = cv2.resize(frame, (0,0), fx=self.fx, fy=self.fx)
            data = pickle.dumps(sframe)
            zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            try:
                self.sock.sendall(struct.pack("L", len(zdata)) + zdata)
            except:
                break
            for i in range(self.interval):
                self.cap.read()
if __name__ == "__main__":
    c = Video_Client('localhost', 8887, 1, 4)
    c.run()
