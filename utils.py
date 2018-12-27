import socket
import time
from io import BytesIO

def get_file_head(file_size, length=10):
    n = len(str(file_size))
    file_head = str(file_size)
    for _ in range(length - n):
        file_head = '0' + file_head
    return file_head

def get_file_size(file_head):
    for i, s in enumerate(file_head):
        if s != '0':
            file_size = int(file_head[i:])
            break
    return file_size

def read_one_file(file_head, source):
    stream = BytesIO()
    file_size = get_file_size(file_head)
    curr_size = 0
    while True:
        remain_size = file_size - curr_size
        if remain_size > 0:
            data = source.recv(min(remain_size, 1024))
            stream.write(data)
            curr_size += len(data)
        elif remain_size == 0:
            break
        else:
            print('error, remain size less than 0')
    data = stream.getvalue()
    stream.flush()
    return data

   
