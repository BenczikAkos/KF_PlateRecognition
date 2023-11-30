import cv2
import argparse
import os
import re
import csv

import car_recognition
import plate_recognition
from text_recognition import image_to_string
from transform import transformImage
from after_work import clean_string

CarRecognizer = car_recognition.CarRecognition()
PlateRecognizer = plate_recognition.PlateRecognition()


valid_plate_samples = [
    '^[A-Za-z]{3}-\d{3}$', # 3 letters, hyphen, 3 numbers
    '^[A-Za-z]{2} [A-Za-z]{2}-\d{3}$', # 2 letters, space, 2 letters, hyphen, 3 numbers
    '^[A-Za-z]{4,}-\d+$', # At least 4 letters, hyphen, at least 1 number
    '^[A-Za-z]{2} \d{2}-\d{2}$', # 2 letters, space, 2 numbers, hyphen, 2 numbers
    '^OT \d{2}-\d{2}', # First 2 letters are OT, space, 1 number, space, 3 numbers
    '^[A-Za-z] \d{2}[A-Za-z]{2} \d{2}$', # 1 letter, space, 2 numbers and 2 letters, space, 2 numbers
    ] 


def select_result(result_plate, result_transform):
    result_plate = clean_string(result_plate)
    result_transform = clean_string(result_transform)
    plate_valid = False
    transform_valid = False
    for pattern in valid_plate_samples:
        if re.search(pattern, result_plate):
            plate_valid = True

    for pattern in valid_plate_samples:
        if re.search(pattern, result_transform):
            transform_valid = True

    if plate_valid and transform_valid:
        return result_transform
    
    if plate_valid:
        return result_plate
    
    if transform_valid:
        return result_transform
    
    return result_plate if len(result_plate) > len(result_transform) else result_transform

def get_path(directory, file):
    return directory + '/' + file

def get_result_file(filename):
    base_name = filename.split('.')[0]
    return base_name + ".txt"

def process_image(IMAGE_URL):
    image = cv2.imread(IMAGE_URL)

    #car_image = CarRecognizer.getCar(image)

    plate_image = PlateRecognizer.getPlate(image)

    if plate_image is None:
        return ""
    
    transformed_image = transformImage(plate_image)

    plate_text = image_to_string(plate_image)
    plate_text_transfromed = image_to_string(transformed_image)

    result = select_result(plate_text, plate_text_transfromed)
    return result

def main(input_dir, output_dir):
    file_list = os.listdir(input_dir)
    total_files = len(file_list)

    with open(output_dir + '/result.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write header row, if desired
        csvwriter.writerow(['Filename', 'Result'])
        for index, image_src in enumerate(file_list):
            result = process_image(get_path(input_dir, image_src))
            csvwriter.writerow([image_src, result.rstrip('\n')])

            percent_complete = int((index / total_files) * 100)

            # Create the loading line display, e.g., [####    ]
            loading_line = '[' + '#' * (percent_complete // 10) + ' ' * ((100 - percent_complete) // 10) + ']'

            # Print the loading line with a carriage return to overwrite the current line
            # end='' prevents the default newline character after the print
            print(f'\r{loading_line} {percent_complete}%', end='')

        loading_line = '[' + '#' * 10 + ' ' * (0) + ']'
        print(f'\r{loading_line} {100}%', end='')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some paths.")

    parser.add_argument("--input", help="Input directory path", default="./dataset/source")
    parser.add_argument("--output", help="Output directory path", default="./dataset")
    args = parser.parse_args()

    main(args.input, args.output)