# import required packages
import cv2
import numpy as np

class Yolo:
    
    args = {'class':'yolo/yolov3.txt','config':'yolo/yolov3.cfg',
        'weights':'yolo/yolov3.weights'}

    path = 'ex_'
    scale = 0.00392
    net = cv2.dnn.readNet(args['weights'], args['config'])
    classes = None
    blob = None
    img = None

    def __init__(self):
        with open(self.args['class'], 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def set_img(self, img_path):
        self.img_path = img_path
        self.img = cv2.imread(img_path)
        
        self.blob = cv2.dnn.blobFromImage(self.img, self.scale, (416,416), (0,0,0), True, crop=False)
        self.net.setInput(self.blob)

    def get_output(self):
        # run inference through the network
        # and gather predictions from output layers
        outs = self.net.forward(self.get_output_layers())
        Width = self.img.shape[1]
        Height = self.img.shape[0]

        # initialization
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        # for each detetion from each output layer 
        # get the confidence, class id, bounding box params
        # and ignore weak detections (confidence < 0.5)
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
        
        # apply non-max suppression
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        # go through the detections remaining
        # after nms and draw bounding box
        for i in indices:
            i = i[0]
            box = boxes[i]
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]
    
            self.draw_bounding_box(self.img, class_ids[i], confidences[i],
                              round(x), round(y), round(x+w), round(y+h))
        
        cv2.imwrite(self.path + self.img_path, self.img)
        print('Successfully save yolo data - {}'.format(self.path + self.img_path))

        return self.img

    def get_output_layers(self):

        net = self.net
        
        layer_names = net.getLayerNames()
    
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers

# function to draw bounding box on the detected object with class name
    def draw_bounding_box(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):

        label = str(self.classes[class_id])

        color = self.COLORS[class_id]

        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
if __name__ == '__main__':

    path = 'test_img2.jpg'

    yolo = Yolo()
    yolo.set_img(path)
    img = yolo.get_output()

    # display output image    
    cv2.imshow("original", cv2.imread(path))
    cv2.imshow("object detection", img)

    # wait until any key is pressed
    cv2.waitKey()

    # release resources
    cv2.destroyAllWindows()