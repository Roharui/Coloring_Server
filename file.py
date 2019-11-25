
import os
import socket
import time
from cv2 import imread

class File:
    base_path = "data/"
    extra_path = 'ex_data/'
    after_path = 'after_data/'
    buffer = 1024
    img = None
    mask = None
    def __init__(self, addr):
        str_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        self.name = self.base_path + str_time + ".png"
        self.exname = self.extra_path + str_time + ".png"
        self.afname = self.after_path + str_time + ".png"
        self.addr = addr
    
    def getName(self):
        return self.name
    
    def file_remove(self, path):
        if os.path.exists(path):
            os.remove(path)
    #
    def getFile(self, data):
        f = open(self.name, 'wb')
        for i in data:
            f.write(i)
        f.close()
        self.img = imread(self.name)
    #
    def strFile(self):
        with open(self.exname,'rb') as f:
            return f.read()

    def strAfterFile(self):
        with open(self.afname,'rb') as f:
            return f.read()

    def delFile(self):
        self.file_remove(self.name)
        self.file_remove(self.exname)
        self.file_remove(self.afname)
    
    
'''
    def recvFile(self):
        self.s.send(b'recving')
        with open(self.name, "wb") as f:
            tmp = self.s.recv(self.buffer)
            while tmp != b'done':
                f.write(tmp)
                self.s.send(b" ")
                tmp = self.s.recv(self.buffer)
'''

'''
    def sendFile(self):
        if os.path.exists(self.exname):
            self.s.send(b'sending')
        else:
            self.s.send(b'NoFileError')
            return
        with open(self.exname, "rb") as f:
            _ = f.read(self.buffer)
            while _:
                self.s.send(_)
                self.s.recv(self.buffer)
                _ = f.read(self.buffer)
            self.s.send(b'done')
'''