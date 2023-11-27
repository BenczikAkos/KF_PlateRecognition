import cv2

import car_recognition
import plate_recognition
import transform
import argparse
import os
import re

CarRecognizer = car_recognition.CarRecognition()
PlateRecognizer = plate_recognition.PlateRecognition()
#OCR = orc.OCR() - inicializálni az OCR-t

valid_plate_samples = [
    '^[A-Za-z]{3}-\d{3}$', # 3 letters, hyphen, 3 numbers
    '^[A-Za-z]{2} [A-Za-z]{2}-\d{3}$', # 2 letters, space, 2 letters, hyphen, 3 numbers
    '^[A-Za-z]{4,}-\d+$', # At least 4 letters, hyphen, at least 1 number
    '^[A-Za-z]{2} \d{2}-\d{2}$', # 2 letters, space, 2 numbers, hyphen, 2 numbers
    '^OT \d \d{3}-', # First 2 letters are OT, space, 1 number, space, 3 numbers hyphen
    '^OT \d{3} \d{3}$', # First 2 letters are OT, space, 3 numbers, space, 3 numbers
    '^[A-Za-z] \d{2}[A-Za-z]{2} \d{2}$', # 1 letter, space, 2 numbers and 2 letters, space, 2 numbers
    ] 


def select_result(result_plate, result_transform):
    plate_valid = False
    transform_valid = False
    for pattern in valid_plate_samples:
        if re.search(pattern, result_plate):
            plate_valid = True

    for pattern in valid_plate_samples:
        if re.search(pattern, result_transform):
            transform_valid = True

    if plate_valid and transform_valid:
        return result_plate if len(plate_valid) > len(transform_valid) else result_transform
    
    if plate_valid:
        return result_plate
    
    if transform_valid:
        return result_transform
    
    return result_plate if len(plate_valid) > len(transform_valid) else result_transform

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

    cv2.imshow("Plate Image", plate_image)
    cv2.imshow("Transformed Image", transformed_image)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # result = select_result(getString_OCR(plate_image), getString_OCR(transformed_image)) - meghívni az OCR-t
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

    # Call only one picture
    # URL = "./dataset/source/..."
    # print(process_image(URL))