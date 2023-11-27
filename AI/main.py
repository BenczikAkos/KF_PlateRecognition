import cv2

import car_recognition
import plate_recognition
import transform
import argparse
import os

CarRecognizer = car_recognition.CarRecognition()
PlateRecognizer = plate_recognition.PlateRecognition()
#OCR = orc.OCR() - inicializálni az OCR-t

def get_path(directory, file):
    return directory + '/' + file

def get_result_file(filename):
    base_name = filename.split('.')[0]
    return base_name + ".txt"

def process_image(IMAGE_URL):
    image = cv2.imread(IMAGE_URL)

    car_image = CarRecognizer.getCar(image)

    plate_image = PlateRecognizer.getPlate(car_image)

    transformed_image = transform.transformImage(plate_image)

    # result = getString_OCR(transformed_image) - meghívni az OCR-t
    # if result == "":
    #   result = getString_OCR(plate_image) - ha nem sikerül a transform, próba az eredetivel
    # return result
    return "xoxo" # törölni

def main(input_dir, output_dir):
    for image_src in os.listdir(input_dir):
        result = process_image(get_path(input_dir, image_src))
        with open(get_path(output_dir, get_result_file(image_src)), 'w') as file:
            file.write(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some paths.")

    # Adding arguments with default values
    parser.add_argument("--input", help="Input directory path", default="./dataset/source")
    parser.add_argument("--output", help="Output directory path", default="./dataset/done")

    # Parse arguments
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(args.input, args.output)