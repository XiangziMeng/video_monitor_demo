import socket
import time
import cv2
from threading import Thread
from multiprocessing import Process
from utils import *

def client_work(sock, fps=True):
    t0 = time.time()
    i = 0
    while True:
        file_head = sock.recv(10)
        filename = './pictures/%d.png' % (i % 200)
        with open(filename, 'wb') as fp:
            data = read_one_file(file_head, sock) 
            fp.write(data)
        img = cv2.imread(filename)
        cv2.imshow("camera", img)
        cv2.waitKey(1)
        i += 1
        if fps and i % 20 == 0:
            seconds = time.time() - t0
            t0 = time.time()
            print('Time: %s, FPS: %f' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), (20 / seconds)))

def client_say_hi(sock):
    while True:
        try:
            sock.sendall(b"hi!")
            time.sleep(1) 
        except Exception as e:
            sock.sendall(b"bye")
            break
    sock.close()
    print('finish haha')

if __name__ == "__main__":
    HOST, PORT = '192.168.1.167', 65432 
    
    # connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    sock_heart_beat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_heart_beat.connect((HOST, PORT))
   
    # open camera window
    cv2.namedWindow("camera")
    
    # start receiving images and displaying them, also send heart beat to server
    t1 = Thread(target=client_say_hi, args=(sock_heart_beat, ))
    t1.start()
    client_work(sock)
    t1.join()

    # close connections
    sock.close()
    sock_heart_beat.close()
    cv2.destroyAllWindows()
    print('finish')
