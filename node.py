
import socket

class Node:
    buffer = 1024
    def __init__(self, conn):
        self.conn = conn
        self.ok = b'@ROK#'
    
    def save(self):
        started = True
        self.data = []
        tmp = self.conn.recv(self.buffer)
        while tmp != b'DONE':
            self.data.append(tmp)
            if started:
                self.conn.send(b'@SOK#')
                started = False
            else:
                self.conn.send(self.ok)
            tmp = self.conn.recv(self.buffer)

    def save_blue(self):
        self.data = []
        tmp = self.conn.recv(self.buffer)
        while tmp != b'done\r\n':
            self.data.append(tmp)
            self.conn.send(self.ok)
            tmp = self.conn.recv(self.buffer)

    def pars_filedata(self):
        try:
            return self.data[1:]
        except IndexError:
            return None

    def command(self):
        return self.data[0].decode("euc-kr")

    def getData(self):
        return [x.decode("euc-kr") for x in self.data[1:]]

    def sendData(self, data):
        datas = [data[i:i+self.buffer] for i in range(0, len(data), self.buffer)]
        for i in datas:
            #i = b'@' + i + b'#'
            self.conn.send(i)
            self.conn.recv(self.buffer)
        self.conn.send(b'@DONE#')

    def sendIMG(self, data):
        datas = [data[i:i+self.buffer - 7] for i in range(0, len(data), self.buffer - 7)]
        for i in datas:
            i = b'@IMG' + i + b'###'
            self.conn.send(i)
            x = self.conn.recv(self.buffer)
        self.conn.send(b'@DONE#')
