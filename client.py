import socket
import time
import cv2
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
        if fps and i % 10 == 0:
            seconds = float(time.time() - t0)
            print('Time: %.2fs, FPS: %f' % (seconds, i / seconds))

if __name__ == "__main__":
    HOST, PORT = '192.168.1.167', 65432
    
    # connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    
    # open camera window
    cv2.namedWindow("camera")
    
    # start receiving and displaying images
    client_work(sock)

    # close connections
    sock.close()
    cv2.destroyAllWindows()
