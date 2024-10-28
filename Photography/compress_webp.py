import os
from PIL import Image

def compress_and_resize_image(input_image_path, output_image_path, max_resolution=(3840, 2160), quality=80):
    # Open the image file
    with Image.open(input_image_path) as img:
        # Check current size
        width, height = img.size
        print(f"Original size of {input_image_path}: {width}x{height}")

        # Calculate new size maintaining the aspect ratio
        if width > max_resolution[0] or height > max_resolution[1]:
            aspect_ratio = width / height
            
            if aspect_ratio > 1:  # Width is greater than height
                new_width = max_resolution[0]
                new_height = int(max_resolution[0] / aspect_ratio)
            else:  # Height is greater than or equal to width
                new_height = max_resolution[1]
                new_width = int(max_resolution[1] * aspect_ratio)

            # Resize the image
            img = img.resize((new_width, new_height), Image.LANCZOS)
            print(f"Resized to {new_width}x{new_height}")

        # Save the image as WebP with specified quality
        img.save(output_image_path, format='WEBP', quality=quality)
        print(f"Saved compressed image: {output_image_path}")

def process_images(directory, max_resolution=(3840, 2160), quality=80):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.webp'):
                input_path = os.path.join(root, file)
                output_path = os.path.splitext(input_path)[0] + '.webp'
                
                print(f'Processing {input_path}...')
                
                # Get original file size
                original_size = os.path.getsize(input_path)

                compress_and_resize_image(input_path, output_path, max_resolution, quality)

                # Get new file size
                new_size = os.path.getsize(output_path)

                # Calculate size reduction percentage
                reduction_percentage = 100 * (original_size - new_size) / original_size if original_size > 0 else 0
                print(f"Size reduction: {reduction_percentage:.2f}%")

if __name__ == '__main__':
    # Set your directory and desired quality here
    target_directory = 'Resources'  # Change this to your target directory
    max_resolution = (3840, 2160)  # Maximum resolution for 4K
    quality = 80  # Compression quality (0-100)

    process_images(target_directory, max_resolution, quality)
