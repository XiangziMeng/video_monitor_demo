from Queue import Queue
from threading import Thread
from random import random
from picamera import PiCamera
from io import BytesIO
from utils import *
import time
import socket

def producer(queue, clock):
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (640, 480)
    camera.start_preview()
    stream = BytesIO()
    for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
        if clock.is_alive():
            data = stream.getvalue() 
            stream.truncate()
            stream.seek(0)
            try:
                queue.put(data, block=True, timeout=0.01)
            except Exception as e:
                time.sleep(0.01)
        else:
            break
    camera.close()
    print('camera close')

def consumer(queue, client, clock):
    while clock.is_alive():
        try:
            data = queue.get(block=True, timeout=0.2)
            file_head = get_file_head(len(data))
            client.sendall(file_head + data)
        except Exception as e:
            time.sleep(0.01)
    client.close()
    print('consumer close')

def receive_heart_beat(client_heart_beat):
    t0 = time.time()
    client_heart_beat.settimeout(2)
    while time.time() - t0 < 5:
        try:
            response = client_heart_beat.recv(3)
            if response == b'hi!':
                t0 = time.time()
                time.sleep(1)
            elif response == b'bye':
                break
        except Exception as e:
            time.sleep(1)
    client_heart_beat.close()
    print('receive heart beat close')

def send_heart_beat(client):
    client.settimeout(2)
    while True:
        try:
            client.sendall('')
            time.sleep(1)
        except Exception as e:
            break
    print('send heart beat close')

if __name__ == "__main__":
    # build a server
    HOST, PORT = '192.168.1.167', 65432
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(2)
    
    # connect to the client
    client, client_addr = sock.accept()
    print('Connected by', client_addr)

    client_heart_beat, client_heart_beat_addr = sock.accept()
    print('Connected by', client_heart_beat_addr)
    
    # initialize a queue of images
    data_queue = Queue(maxsize=5)
    
    # run producer, consumer and receive_heart_beat
    threads = []
    threads.append(Thread(target=receive_heart_beat, args=(client_heart_beat, )))
    threads.append(Thread(target=producer, args=(data_queue, threads[0])))
    threads.append(Thread(target=consumer, args=(data_queue, client, threads[0])))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # close the server
    sock.close()
