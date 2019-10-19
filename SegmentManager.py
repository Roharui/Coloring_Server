
#this code is from https://www.pyimagesearch.com/2018/09/03/semantic-segmentation-with-opencv-and-deep-learning/

import numpy as np
import imutils
import time
import cv2

class SegmentManager:
    def __init__(self):
        self.args = {'model':"enet-cityscapes/enet-model.net",
                     'classes':"enet-cityscapes/enet-classes.txt ",
                      'colors':"enet-cityscapes/enet-colors.txt "}

        self.classes = open(self.args["classes"]).read().strip().split("\n")

        COLORS = open(self.args["colors"]).read().strip().split("\n")
        COLORS = [np.array(c.split(",")).astype("int") for c in COLORS]

        self.COLORS = np.array(COLORS, dtype="uint8")

        self.net = cv2.dnn.readNet(self.args["model"])

        self.mask = np.zeros([1,1], dtype=bool)

    def set_img(self, file):
        self.file = file
        self.img_path = file.getName()
        self.image = file.img
        image = imutils.resize(self.image, width=500)
        self.blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (1024, 512), 0,
            swapRB=True, crop=False)

    def get_output(self):
        self.net.setInput(self.blob)
        output = self.net.forward()
        #(numClasses, height, width) = output.shape[1:4]
        classMap = np.argmax(output[0], axis=0)
        mask = self.COLORS[classMap]
        mask = cv2.resize(mask, (self.image.shape[1], self.image.shape[0]),
	        interpolation=cv2.INTER_NEAREST)

        self.file.mask = mask
        #self.mask = mask

        classMap = cv2.resize(classMap, (self.image.shape[1], self.image.shape[0]),
            interpolation=cv2.INTER_NEAREST)
        output = ((0.4 * self.image) + (0.6 * mask)).astype("uint8")

        cv2.imwrite(self.file.exname, output)
        print('Successfully save segment data - {}'.format(self.file.exname))

    def getSimiler(self):
        x, y = self.xy
        self.fmask = self.file.mask
        mask = np.zeros(self.fmask.shape[:-1], dtype=bool)
        mask[x][y] = True
        arr1 = []
        arr2 = [[x, y]]
        while len(arr2) != 0:
            for i, j in arr2:
                arr1 += self.closeMask(mask, i, j)
            arr2.clear()
            arr1 = np.unique(np.array(arr1), axis=0)
            for i, j in arr1:
                if np.array_equal(self.fmask[x][y],self.fmask[i][j]):
                    mask[i][j] = True
                    arr2.append([i,j])
            arr1 = []

        return mask[:,:,np.newaxis]

    def closeMask(self, mask,x,y):
        result = []
        abc = [[0,1],[1,0],[-1,0],[0,-1]]
        for i, j in abc:
            if x + i >= self.fmask.shape[0] or x + i < 0 or y + j >= self.fmask.shape[1] or y + j < 0:
                continue
            if not mask[x + i][y + j]:
                result.append((x + i, y + j))
        return result

    def colorFilter(self):
        color = np.array(self.color)
        cFilter = np.where(self.getSimiler(),
                             (((1 - self.a) * self.image) + (self.a * color)).astype("uint8"),
                             self.image)

        return cFilter

    def setXY(self, xy):
        self.xy = list(map(int, xy))

    def setColor(self, color):
        self.a = color[-1]
        color = list(map(int, color[:-1]))
        self.color = [color[-1], color[1], color[0]]
        

    def setFile(self, file):
        self.file = file

    def do(self):
        cv2.imwrite(self.file.afname, self.colorFilter())
        print('Successfully filterd data - {}'.format(self.file.afname))


    def set_img_test(self, img):
        self.img_path = img
        self.image = cv2.imread(img)

        image = imutils.resize(self.image, width=500)
        self.blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (1024, 512), 0,
            swapRB=True, crop=False)
        

if __name__ == '__main__':

    s = SegmentManager()

    dfdf = cv2.imread("client/test_img2.jpg")
    print(dfdf.shape)

    s.set_img_test("client/test_img2.jpg")
    s.get_output()
    s.xy = (10, 10)
    s.getSimiler()
    s.setColor((0,0,0,0.5))
    x = s.colorFilter()
    print(x.shape)
    cv2.imshow("ddd", s.mask)
    cv2.imshow("mask", x)
    cv2.waitKey(0)
    