import os

def delete_files(directory, keep_count=400):
    # Ensure the provided directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    # List all files in the directory
    files = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

    # Sort files by creation time or any other criteria if needed
    files.sort()

    # Keep only the first 400 files
    files_to_delete = files[keep_count:]

    # Delete the rest of the files
    for file in files_to_delete:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")

# Replace 'path_to_directory' with the path of your directory
directory_path = './valid_result'
delete_files(directory_path)