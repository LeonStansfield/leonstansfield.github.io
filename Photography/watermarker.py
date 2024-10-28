import os
from PIL import Image, ImageDraw, ImageFont, ExifTags

def process_image(input_image_path, output_image_path, watermark_text, max_resolution=(3840, 2160), font_size=100, quality=80):
    # Open the image file and handle orientation via EXIF
    with Image.open(input_image_path) as img:
        # Apply EXIF orientation
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        if hasattr(img, '_getexif') and img._getexif() is not None:
            exif = img._getexif()
            if exif is not None and orientation in exif:
                if exif[orientation] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    img = img.rotate(90, expand=True)

        # Resize the image if it exceeds the max resolution, maintaining aspect ratio
        width, height = img.size
        aspect_ratio = width / height
        if width > max_resolution[0] or height > max_resolution[1]:
            if aspect_ratio > 1:  # Landscape
                new_width = max_resolution[0]
                new_height = int(max_resolution[0] / aspect_ratio)
            else:  # Portrait or square
                new_height = max_resolution[1]
                new_width = int(max_resolution[1] * aspect_ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
            print(f"Resized to: {new_width}x{new_height}")

        # Create a transparent layer for the watermark
        watermark_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(watermark_layer)
        
        # Load the font and calculate text dimensions
        font_path = "Roboto-Black.ttf"  # Update with the path to your TTF font file
        font = ImageFont.truetype(font_path, font_size)
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Position the watermark in the center of the image
        x = (img.width - text_width) / 2
        y = (img.height - text_height) / 2

        # Draw the watermark text onto the transparent layer
        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 15))  # Adjust opacity (last number in RGBA)

        # Composite the watermark layer onto the image
        watermarked_image = Image.alpha_composite(img.convert("RGBA"), watermark_layer)

        # Save the result as WebP with compression
        watermarked_image = watermarked_image.convert("RGB")  # Convert back to RGB to save as WebP
        watermarked_image.save(output_image_path, format='WEBP', quality=quality)
        print(f"Processed and saved: {output_image_path}")

def process_images(directory, watermark_text, max_resolution=(3840, 2160), font_size=100, quality=80):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                input_path = os.path.join(root, file)
                output_path = os.path.splitext(input_path)[0] + '.webp'

                print(f"Processing {input_path}...")

                # Calculate original file size
                original_size = os.path.getsize(input_path)

                # Process the image (resize, watermark, save as WebP)
                process_image(input_path, output_path, watermark_text, max_resolution, font_size, quality)

                # Calculate new file size and reduction percentage
                new_size = os.path.getsize(output_path)
                reduction_percentage = 100 * (original_size - new_size) / original_size if original_size > 0 else 0
                print(f"Size reduction: {reduction_percentage:.2f}%")

                # Delete the original file
                #os.remove(input_path)
                #print(f"Deleted original file: {input_path}")

if __name__ == '__main__':
    # Set the directory, watermark text, and parameters
    target_directory = 'Resources'  # Replace with your directory path
    watermark_text = 'Leon Stansfield'
    max_resolution = (3840, 2160)  # 4K resolution
    font_size = 300
    quality = 80  # WebP quality

    process_images(target_directory, watermark_text, max_resolution, font_size, quality)
