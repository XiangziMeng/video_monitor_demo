import socket
import time
from io import BytesIO
from utils import *


def transfer_work(sock, source, client):    
    source.sendall('client  online')
    while True:
        file_head = source.recv(10)
        data = read_one_file(file_head, source)
        try:
            client.sendall(file_head + data)
            source.sendall('client  online')
        except Exception as ex:
            try:
                source.sendall('client offline')
                client, client_addr = sock.accept()
                print("Client Connected by", client_addr)
                source.sendall('client  online')
            except KeyboardInterrupt as key:
                print("Interrupted")
                source.sendall('shut down boys')
                break
    
    source.close()
    client.close()
    sock.close()
   
    
if __name__ == "__main__":
    HOST, PORT = '192.168.1.167', 65432
   
    # build server 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(2)

    # connect to source and client
    source, source_addr = sock.accept()
    print("Source Connected by", source_addr)
    client, client_addr = sock.accept()
    print("Client Connected by", client_addr)

    # start working
    transfer_work(sock, source, client)    

