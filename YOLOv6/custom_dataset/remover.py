import os

places = {"train", "val", "test"}

for subfolder in places:
    picture_folder = f"./images/{subfolder}"
    txt_folder = f"./labels/{subfolder}"

    # Get a list of all txt files (excluding directories) in the txt folder
    txt_files = [f for f in os.listdir(txt_folder) if os.path.isfile(os.path.join(txt_folder, f))]

    # Iterate through each file in the picture folder
    for picture_file in os.listdir(picture_folder):
        picture_path = os.path.join(picture_folder, picture_file)

        # Check if the corresponding txt file exists
        txt_file = picture_file.replace(".jpg", ".txt")  # adjust the extension accordingly
        if txt_file not in txt_files:
            # Delete the picture file if there's no corresponding txt file
            os.remove(picture_path)
            print(f"Deleted: {picture_path}")
