import os
import csv

def compare_result_with_file(result, file_path):
    """Compares a result string with the contents of a file."""
    with open(file_path, 'r') as f:
        return result.strip() == f.read().strip()

def count_matching_results(csv_file, validate_dir):
    """Counts the number of matching results from the CSV file with the text files in the validation directory."""
    matching_results = 0
    number_of_entries = 0

    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename = row['Filename']
            result = row['Result']
            validate_path = os.path.join(validate_dir, filename.replace('.jpg', '') + '.txt')

            if os.path.isfile(validate_path):
                if compare_result_with_file(result, validate_path):
                    matching_results += 1

            number_of_entries += 1

    return matching_results, number_of_entries

def main():
    csv_file = './result.csv' 
    validate_dir = './valid_result'

    matching, all_entries = count_matching_results(csv_file, validate_dir)
    print(f'Number of matching results: {matching}')
    print(f'Number of all entries: {all_entries}')
    print(f'Accuracy: {matching / all_entries:.2f} - {round(matching / all_entries * 100, 2)} %')

if __name__ == "__main__":
    main()