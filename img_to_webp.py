import os

# Define the supported image extensions for deletion
DELETE_EXTENSIONS = ('.jpg', '.jpeg', '.png')

# Function to delete files with specific extensions in a directory
def delete_images_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(DELETE_EXTENSIONS):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    # Specify the directory to traverse
    directory = "Posts"

    # Delete all .jpg, .jpeg, and .png files in the directory and subdirectories
    delete_images_in_directory(directory)
