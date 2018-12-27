#coding: utf-8
from picamera import PiCamera
from io import BytesIO
import time
import socket
import os
from utils import *


def take_picture(camera, stream, width, height):
    camera.resolution = (width, height)
    camera.rotation = 180
    camera.capture(stream, 'jpeg')

def source_work(sock):
    flag = b'client offline'
    while True:
        signal = sock.recv(14)
        if signal == b'shut down boys':
            break
        elif signal == b'client offline':
            flag = b'client offline'
            time.sleep(2)
            continue
        elif signal == b'client  online' or flag == b'client  online':
            flag = b'client  online'
        elif flag == b'client offline':
            time.sleep(2)
            continue
        try:
            stream = BytesIO()
            take_picture(camera, stream, 640, 480)
            
            data = stream.getvalue()
            file_head = get_file_head(len(data))
            
            sock.sendall(file_head + data)
            stream.flush()
        except KeyboardInterrupt:
            print('keyboard interrupt')
            break


if __name__ == "__main__":
    # open camera
    camera = PiCamera()
    camera.start_preview()
    time.sleep(2)
    
    # connect to server
    HOST, PORT = '192.168.1.167', 65432 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    # start transferring
    source_work(sock)
    
    # close connections
    sock.close()
    camera.close()
