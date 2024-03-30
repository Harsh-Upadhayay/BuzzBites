import os
from PIL import Image
import hashlib

def calculate_image_hash(image_path):
    """
    Calculate the hash of an image file.
    """
    with open(image_path, 'rb') as f:
        image_hash = hashlib.md5(f.read()).hexdigest()
    return image_hash

def find_unique_images(directory):
    """
    Find unique images in the specified directory.
    """
    unique_images = set()
    duplicate_images = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is an image
            if any(file.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
                file_path = os.path.join(root, file)
                image_hash = calculate_image_hash(file_path)

                # Check if the hash is already encountered
                if image_hash in unique_images:
                    duplicate_images.append(file_path)
                else:
                    unique_images.add(image_hash)

    return unique_images, duplicate_images

if __name__ == "__main__":
    directory_path = '../data'
    unique_images, duplicate_images = find_unique_images(directory_path)

    print("Unique Images:")
    print(len(unique_images))

    print("\nDuplicate Images:")
    print(len(duplicate_images))
