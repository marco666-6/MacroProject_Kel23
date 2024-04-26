import os

def find_duplicate_files(directory):
    # Create a dictionary to store base file names as keys and lists of their corresponding full file paths as values
    file_dict = {}

    # Iterate through the files in the directory
    for filename in os.listdir(directory):
        # Get the full file path
        full_path = os.path.join(directory, filename)

        # Check if the file is a regular file (not a directory)
        if os.path.isfile(full_path):
            # Get the base file name (without the extension)
            base_name = os.path.splitext(filename)[0]

            # Add the full file path to the list for the corresponding base name
            if base_name in file_dict:
                file_dict[base_name].append(full_path)
            else:
                file_dict[base_name] = [full_path]

    # Filter the dictionary to only include base names with more than one file
    duplicate_files = {base_name: paths for base_name, paths in file_dict.items() if len(paths) > 1}

    return duplicate_files

# Specify the directory path you want to check
directory_to_check = 'c:/Users/LENOVO/Desktop/PBL-AI/pbl/Datasets'

duplicate_files = find_duplicate_files(directory_to_check)
Total = 0

if duplicate_files:
    print("Duplicate files with the same base name found:")
    for base_name, paths in duplicate_files.items():
        print(f"Base Name: {base_name}, Count: {len(paths)}")
        if len(paths) > 0 :
            Total += 2
            print(Total)
        for path in paths:
            print(f"  - {path}")

else:
    print("No duplicate files with the same base name found.")

