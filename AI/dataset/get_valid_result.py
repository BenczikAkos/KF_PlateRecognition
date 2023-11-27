import re
import csv


def extract_number_from_url(url):
    match = re.search(r'/(\d+)\.jpg$', url)
    if match:
        return match.group(1)
    return None

def save_plate_to_file(csv_file_path, output_directory):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            plate_number = row['Plate number']
            image_url = row['Image']
            file_number = extract_number_from_url(image_url)

            if file_number:
                file_path = f"{output_directory}/{file_number}.txt"
                with open(file_path, 'w') as file:
                    file.write(plate_number)

def main():
    input_csv = './KF_HF_train_dataset.csv' 
    output_dir = './valid_result' 

    save_plate_to_file(input_csv, output_dir)

if __name__ == "__main__":
    main()