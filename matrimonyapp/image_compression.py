import os
from PIL import Image
import tensorflow as tf

def compress_image_pillow(input_path, output_path='compressed_image.jpg', target_size=(128, 128)):
    """Compress an image using Pillow without reducing quality significantly."""
    with Image.open(input_path) as img:
        img = img.resize(target_size, Image.LANCZOS)
        # Convert to JPEG if it's a PNG to save space
        if img.format == 'PNG':
            output_path = output_path.replace('.png', '.jpg')
            img = img.convert('RGB')  # Convert PNG to RGB before saving as JPEG
        img.save(output_path, 'JPEG', quality=90)  # Use higher quality
        print(f"Compressed image saved to {output_path}")

def compress_images_in_folder_pillow(folder_path, output_folder, target_size=(128, 128)):
    """Compress all images in a folder using Pillow."""
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, f'compressed_{filename}')
            compress_image_pillow(input_path, output_path, target_size)

def compress_with_tensorflow(input_path, output_path='compressed_image_tf.jpg', target_size=(128, 128)):
    """Compress an image using TensorFlow without reducing quality significantly."""
    img = tf.io.read_file(input_path)
    img = tf.image.decode_image(img)
    img = tf.image.resize(img, target_size)
    img = tf.clip_by_value(img, 0, 255)  # Ensure pixel values are in range
    img = tf.cast(img, tf.uint8)  # Cast to uint8 for saving
    tf.keras.preprocessing.image.save_img(output_path, img, quality=95)  # Use higher quality
    print(f"Compressed image saved to {output_path}")

def compress_images_in_folder_tf(folder_path, output_folder, target_size=(128, 128)):
    """Compress all images in a folder using TensorFlow."""
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, f'compressed_tf_{filename}')
            compress_with_tensorflow(input_path, output_path, target_size)

