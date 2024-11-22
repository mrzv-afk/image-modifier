from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
import random
import os

def modify_image(image_path, output_path=None):
    img = Image.open(image_path)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    img_array = np.array(img)
    
    noise = np.random.randint(-15, 15, img_array.shape)
    img_array = np.clip(img_array + noise, 0, 255)
    
    color_shift = np.random.uniform(0.95, 1.05, 3)
    img_array = img_array * color_shift
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)
    
    modified_img = Image.fromarray(img_array)
    
    modified_img = modified_img.filter(ImageFilter.BLUR)
    modified_img = modified_img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
    
    width, height = modified_img.size
    new_width = width + random.randint(-10, 10)
    new_height = height + random.randint(-10, 10)
    modified_img = modified_img.resize((new_width, new_height))
    
    enhancer = ImageEnhance.Brightness(modified_img)
    modified_img = enhancer.enhance(random.uniform(0.95, 1.05))
    
    enhancer = ImageEnhance.Contrast(modified_img)
    modified_img = enhancer.enhance(random.uniform(0.95, 1.05))
    
    enhancer = ImageEnhance.Color(modified_img)
    modified_img = enhancer.enhance(random.uniform(0.95, 1.05))
    
    modified_img = modified_img.filter(ImageFilter.GaussianBlur(radius=0.3))
    
    if output_path is None:
        directory = os.path.dirname(image_path)
        filename = os.path.basename(image_path)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(directory, f"{name}_modified{ext}")
    
    modified_img.save(output_path, optimize=True, exif=b"")
    
    return output_path

def process_directory(input_dir, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(input_dir, 'modified')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    
    processed_files = []
    for filename in os.listdir(input_dir):
        if any(filename.lower().endswith(fmt) for fmt in supported_formats):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"modified_{filename}")
            try:
                modify_image(input_path, output_path)
                processed_files.append(output_path)
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {str(e)}")
    
    return processed_files

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Использование:")
        print("Для одного файла: python image_modifier.py путь_к_изображению")
        print("Для директории: python image_modifier.py путь_к_директории -d")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    if len(sys.argv) > 2 and sys.argv[2] == '-d':
        if os.path.isdir(input_path):
            processed = process_directory(input_path)
            print(f"Обработано {len(processed)} файлов")
        else:
            print("Указанный путь не является директорией")
    else:
        if os.path.isfile(input_path):
            output_path = modify_image(input_path)
            print(f"Изображение обработано и сохранено: {output_path}")
        else:
            print("Указанный файл не существует")
