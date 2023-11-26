import cv2
import numpy as np
import os


class CarRecognition:

    def __init__(self):
        WORKING_DIR = os.getcwd()
        CONFIG_FILE = WORKING_DIR + '/car_recognition.cfg'
        WEIGHTS = WORKING_DIR + '/car_recognition.weights'
        CLASSES =  WORKING_DIR + '/car_recognition.txt'

        # Beolvassuk a címkéket a fájlból, és elmentjük.
        self.classes = None
        with open(CLASSES, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]

        # Létrehozzuk az előtanított hálót a súly és a config alapján, majd átalakítjuk a képet és beadjuk bemenetnek a hálónak.
        self.net = cv2.dnn.readNet(WEIGHTS, CONFIG_FILE)

    def getCar(self, image):
        # Elmentjük a magasságát és a szélességét a képnek, majd a scale faktort ami 1/255-nek felel meg. (0..255) -> (0..1)
        Width = image.shape[1]
        Height = image.shape[0]
        scale = 1/255

        blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
        self.net.setInput(blob)

        # Következtetéseket lefuttatjuk a hálón keresztül és az előrejelzéseket kigyűjtjük a kimeneti rétegekből
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        outs = self.net.forward(output_layers)

        # Változók inicializálás
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        # Kimenetek feldolgozása
        for out in outs:
            # detection első 4 paramétere: (középpont) x, y, szélesség, magasság
            for detection in out:
                scores = detection[5:] # Cimkék valószínűségei kigyűjtése
                class_id = np.argmax(scores) # Max valószínűség kiválasztása
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Középpontból kiszámoljuk a bal felső sarkot, és visszaskálázzuk a 0..1-ről a 0..H és 0..W-re az értékeket.
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2 
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        # Non-max suppression használata a kimenetre
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        # Kiválasztjuk a legnagyobb területtel rendelkező találatot a képről
        max_i = -1
        max_area = 0
        for i in indices:
            box = boxes[i]
            current_area = box[2] * box[3]
            if max_area < current_area:
                max_area = current_area
                max_i = i

        # Ha nincs találat kiírjuk, különben levágjuk a találatra a képet és megnyitjuk.
        if max_i == -1:
            return image
        else:
            biggest_box = boxes[max_i]
            x = max(0, int(biggest_box[0]))
            y = max(0, int(biggest_box[1]))
            w = int(biggest_box[2])
            h = int(biggest_box[3])
            return image[y:y+h,x:x+w]

