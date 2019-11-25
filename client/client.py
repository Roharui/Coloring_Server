
import socket

class FileManager:
    buffer = 1024
    def __init__(self, s):
        self.s = s
    def send(self, name):
        s.send(b"ISEND")
        s.recv(self.buffer)

        with open(name, "rb") as f:
            _ = f.read(self.buffer)
            while _:
                self.s.send(_)
                self.s.recv(self.buffer)
                _ = f.read(self.buffer)
        self.s.send(b'DONE')
        
    def recv(self, name):
        s.send(b"IGET")
        s.recv(self.buffer)
        s.send(b'DONE')

        with open(name, "wb") as f:
            tmp = self.s.recv(self.buffer)
            while tmp != b'DONE':
                f.write(tmp)
                self.s.send(b" ")
                tmp = self.s.recv(self.buffer)
    
    def delete(self):
        self.s.send(b'DFILE')
        print(self.s.recv(self.buffer))
        self.s.send(b'DONE')

    def color_data(self):
        self.s.send(b'CDATA')
        self.s.recv(self.buffer)
    
        self.s.send('255,0,0'.encode())
        self.s.recv(self.buffer)
        self.s.send(b'DONE')

        tmp = self.s.recv(self.buffer)
        while tmp != b'DONE':
            print(tmp)
            self.s.send(b" ")
            tmp = self.s.recv(self.buffer)

    def recomment_color(self):
        self.s.send(b'RCDATA')
        self.s.recv(self.buffer)
        self.s.send('255,0,0'.encode())
        self.s.recv(self.buffer)
        self.s.send(b'DONE')
        print(self.s.recv(self.buffer))
        
    def color_filtering(self):
        self.s.send(b'FDATA')
        self.s.recv(self.buffer)
        for i in [10, 10, 255,0,0,0.5]:
            self.s.send(str(i).encode())
            self.s.recv(self.buffer)
        self.s.send(b'DONE')

        with open("test.png", "wb") as f:
            tmp = self.s.recv(self.buffer)
            while tmp != b'DONE':
                f.write(tmp)
                self.s.send(b" ")
                tmp = self.s.recv(self.buffer)


if __name__ == '__main__':
    s = socket.socket()
    s.connect(("127.0.0.1", 6355))
    fm = FileManager(s)
    #fm.send("test.jpg")
    fm.send("018.jpg")

    fm.recv("test.png")

    #fm.delete()
    #fm.color_data()
    #fm.recomment_color()
    #fm.color_filtering()
    #print(s.recv(1024).decode('utf8'))
    #fm.delete()
    fm.s.close()

    #파일을 보낼때
    #s.send(b"ISEND")
    #data = s.recv(1024)
    #FileManager("i16012365821.jpg").send(s)
    #print(data)

    #파일 받을때
    #s.send(b'IGET')
    #data = s.recv(1024)
    #FileManager("i16012365821.jpg").recv(s)
    #print(data)
