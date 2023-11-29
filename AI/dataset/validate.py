import os

def compare_files(file1, file2):
    """Compares the contents of two files."""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        return f1.read() == f2.read()

def count_matching_files(result_dir, validate_dir):
    """Counts files with the same name and content in two folders."""
    matching_result = 0
    number_of_files = 0

    validators = os.listdir(validate_dir)

    for validator in validators:
        result_path = os.path.join(result_dir, validator)
        validate_path = os.path.join(validate_dir, validator)

        if os.path.isfile(result_path) and os.path.isfile(validate_path):
            if compare_files(result_path, validate_path):
                matching_result += 1

        number_of_files += 1

    return matching_result, number_of_files

def main():
    result_dir = './done' 
    validate_dir = './valid_result'

    matching, all_files = count_matching_files(result_dir, validate_dir)
    print(f'Number of matching files: {matching}')
    print(f'Number of all files: {all_files}')
    print(f'Accuracy: {matching / all_files} - {round(matching / all_files * 100, 2)} %')

if __name__ == "__main__":
    main()