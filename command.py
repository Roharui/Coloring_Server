
import yolo
import file
import numpy as np
import node
from colorManager import ColorManager
from AiManager import AiManager
from SegmentManager import SegmentManager

class Command:
    yolo = yolo.Yolo()
    sm = SegmentManager()
    cm = ColorManager()
    am = AiManager()

    def __init__(self, conn):
        self._node = node.Node(conn)
        self.cmd_list = {'ISEND': self.get_Image,'IGET': self.send_Image,
                         'DFILE': self.del_File, 'CDATA': self.color_data,
                         'RCDATA': self.recommend_data,
                         'FDATA' : self.color_filtering}

    def encodeD(self, data):
        data = b'@' + data.encode() + b'#'
        return data

    def reset(self):
        self._node.save()

    def setFile(self, f):
        self.f = f

    def predict(self):
        self.sm.set_img(self.f)
        self.sm.get_output()
        #self.yolo.set_img(self.f.getName())
        #self.yolo.get_output()

    def getCmd(self):
        print()
        print("Command resived - {0}".format(self._node.command()))
        return self._node.command()

    def do(self):
        self.reset()
        cmd = self.getCmd()
        return self.cmd_list[cmd]()

    #세션 유지 : True, 세션 제거시 : False
    def get_Image(self):
        if self._node.pars_filedata() == None:
            raise NameError("NoDataError")

        self.f.getFile(self._node.pars_filedata())
        print("reciving Success - {0}".format(self.f.addr))
        self.predict()
        print("sending File : {0} - {1}".format(self.f.exname, self.f.addr))
        self._node.sendIMG(self.f.strFile())
        print("sending Success - {0}".format(self.f.addr))
        return True
        
    
    def send_Image(self):
        print("sending File : {0} - {1}".format(self.f.exname, self.f.addr))
        self._node.sendIMG(self.f.strFile())
        print("sending Success - {0}".format(self.f.addr))
        return True
        

    def del_File(self):
        print("delete File : {0} - {1}".format(self.f.name ,self.f.addr))
        self.f.delFile()
        return False

    def color_data(self):
        print("predicting color data - {0}".format(self.f.addr))
        cdata = self._node.getData()
        cdata = [int(i) for i in cdata[0].split(",")]
        s = self.cm.getName(cdata)['name']
        print("color data : {0} - {1}".format(s, cdata))
        s = self.encodeD('N: ' + s)
        self._node.sendData(s)
        return True

    def recommend_data(self):
        print("recommend color data - {0}".format(self.f.addr))
        cdata = self._node.getData()
        s = self.am.do(cdata)
        print("color datas : {0} - {1}".format(s, cdata))
        s = self.encodeD(s)
        self._node.sendData(s)
        return True

    def color_filtering(self):
        print("filtering img as color - {0}".format(self.f.addr))
        data = self._node.getData()
        self.sm.file = self.f
        self.sm.setXY(data[:2])
        self.sm.setColor(data[2:])
        self.sm.do()
        print("sending File : {0} - {1}".format(self.f.afname, self.f.addr))
        self._node.sendData(self.f.strAfterFile())
        print("sending Success - {0}".format(self.f.addr))
        return True
