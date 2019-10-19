
import connect
import sys
import threading
from bluetooth import *

class Server:
    def __init__(self):
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        service_name = "Coloring"

        self.s = BluetoothSocket( RFCOMM )
        self.s.bind(('',PORT_ANY))        

        advertise_service( self.s, service_name,
            service_id = uuid,
            service_classes = [ uuid, SERIAL_PORT_CLASS ],
            profiles = [ SERIAL_PORT_PROFILE ] )

        print("Blutooth Server is starting at : {0}:{1}".format(service_name, uuid))

        x = threading.Thread(target=self.run)
        x.start()

    def run(self):
        while True:
            self.s.listen(5)
            try:
                conn, addr = self.s.accept()
            except Exception:
                pass
            else:
                th = connect.Connection(conn, addr)
                th.start()

if __name__ == '__main__':
    s = Server()