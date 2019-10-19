
import threading, socket
import connect
import sys

class Server:
    def __init__(self, ip, port):

        self.s = socket.socket()
        self.s.bind((ip, port))
        self.s.listen(1)

        print("Server is starting at : {0}:{1}".format(ip, port))

    def run(self):
        while True:
            conn, addr = self.s.accept()
            connect.Connection(conn, addr).start()

if __name__ == '__main__':
    try:
        ip = sys.argv[1]
        port = int(sys.argv[2])
    except IndexError:
        ip = '127.0.0.1'
        port = 6355

    s = Server(ip, port)
    s.run()
