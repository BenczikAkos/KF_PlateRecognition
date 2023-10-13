import cv2 as cv
import argparse
import sys
import numpy as np
import os.path

# MINE Argument parsing
parser = argparse.ArgumentParser(description="Process images from input directory.")

parser.add_argument("input_dir", help="Path to the input directory (required)", required=True)

parser.add_argument("--done_dir", help="Path to the done directory, these will be omitted from input_dir", default=r".\cropped")
parser.add_argument("--cropped_dir", help="Save path of the cropped pictures", default=r".\cropped")
parser.add_argument("--labels", help="Save path of the labels", default=r".\labels")
parser.add_argument("--failed", help="Save path of the failed pictures", default=r".\failed")

args = parser.parse_args()

input_directory = args.input_directory
done_directory = args.done_directory
cropped_dir = args.cropped_dir
labels = args.labels
failed = args.failed

# Initialize the parameters
confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold

inpWidth = 416  # 608     # Width of network's input image
inpHeight = 416  # 608     # Height of network's input image

# Load names of classes
classesFile = "classes.names"

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.

modelConfiguration = "./darknet-yolov3.cfg"
modelWeights = "./model.weights"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def getOutputsNames(net: cv.dnn.Net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawPred(classId, conf, left, top, right, bottom, filename):
    # MINE save the cropped license plates
    lp_cropped = img[top:bottom, left:right]
    croppedOutputFile = os.path.join(cropped_dir, filename)
    if not lp_cropped is None and lp_cropped.shape[0] != 0 and lp_cropped.shape[1] != 0:
        cv.imwrite(croppedOutputFile, lp_cropped.astype(np.uint8))
    # Draw a bounding box.
    cv.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s: %s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(
        label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(img, (left, top - round(1.5*labelSize[1])), (left + round(
        1.5*labelSize[0]), top + baseLine), (255, 0, 255), cv.FILLED)
    
    #cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine),    (255, 255, 255), cv.FILLED)
    cv.putText(img, label, (left, top),
               cv.FONT_HERSHEY_SIMPLEX, 0.70, (255, 255, 255), 2)


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs, filename):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    foundPlate = False
    for out in outs:
        # print("out.shape : ", out.shape)
        for detection in out:
            # if detection[4]>0.001:
            scores = detection[5:]
            classId = np.argmax(scores)
            # if scores[classId]>confThreshold:
            confidence = scores[classId]
            if confidence > confThreshold:
                # MINE saving the detection coordinates to a label txt
                (cx, cy, bbx, bby) = detection[0:4]
                label = f"0 {cx} {cy} {bbx} {bby}"
                outputFile = os.path.join(labels, filename[:-4])
                with open(outputFile + ".txt", 'w') as file:
                    file.write(label)
                # barrier
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
                foundPlate = True
    # MINE ahol semmit nem talált azt külön menti el
    if not foundPlate:
        failed_file_path = os.path.join(failed, filename)
        cv.imwrite(failed_file_path, frame.astype(np.uint8))


    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        # i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(classIds[i], confidences[i], left,
                 top, left + width, top + height, filename)

if __name__ == "__main__":

    all_file_list = os.listdir(input_directory)
    done_list = os.listdir(done_directory)
    file_list = [item for item in all_file_list if item not in done_list]
    allFilesCount = len(file_list)
    for index, filename in enumerate(file_list):
        print(f"{index}/{allFilesCount}")
        img = cv.imread(os.path.join(input_directory, filename))

        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(
            img, 1/255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(getOutputsNames(net))

        # Remove the bounding boxes with low confidence
        postprocess(img, outs, filename)

        # Write the frame with the detection boxes
        outputFile = os.path.join(done_directory, filename)
        cv.imwrite(outputFile, img.astype(np.uint8))
