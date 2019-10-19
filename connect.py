"""
#연결후 동작하는 모듈

#커맨드 객체와 파일 객체 생성
#똑같은 아이피로 접속한 사람은 똑같은 파일 객체 사용
#예외처리도 여기에서 담당

"""


import threading, socket
import file
import command
import node

conn_num = 0
connection_list = []

class Connection(threading.Thread):
    global connection_list
    def __init__(self, connect, addr):
        threading.Thread.__init__(self)

        self.connect = connect
        self.addr, self.num = addr
        
        print("connect at : {0}".format(self.addr))

        self.f = self.find_file()
        self.command = command.Command(connect)
        self.command.setFile(self.f)

    def find_file(self):
        for i in connection_list:
            if i.addr == self.addr:
                print('Using file - {}'.format(i.addr))
                return i
        tmp = file.File(self.addr)
        connection_list.append(tmp)
        return tmp

    def remove_file(self):
        connection_list.remove(self.f)
        self.f.delFile()

    def run(self):
        conn = self.connect
        try:
            while True:
                result = self.command.do()

                if not result:
                    self.remove_file()
                    self.find_file()

        except KeyError:
            print('Error : keyError - {0}'.format(self.addr))
            print("Key : [{0}]".format(self.command.getCmd()))
            conn.send(b'KeyError')
        except NameError as e:
            print("Error : {0} - {1}".format(e.args, self.addr))
            conn.send("{0}".format(e.args).encode())
        except TimeoutError:
            print('Error : TimeOut - {0}'.format(self.addr))
        except FileNotFoundError:
            print('Error : FileNotFound - {0}'.format(self.addr))
            print('File : {0}'.format(self.f.exname))
        except ConnectionAbortedError:
            pass
        except OSError as e:
            print("Error : OSError")
        #except ConnectionError:
        #    print('Error : ConnectionError')
        finally:
            print('disconnet at  : {0}'.format(self.addr))
            print()
            #self.remove_file()
            conn.close()
