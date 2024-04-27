import cv2
import sys
import pyocr
import tempfile
import numpy as np
import pyocr.builders
from PIL import Image

def increase_contrast(image, alpha=1.5, beta=0):
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted_image

def enhance_text_quality(image):
    # Увеличение резкости изображения
    sharpened_image = cv2.filter2D(image, -1, kernel=np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))
    # Уменьшение размытия текста
    return cv2.GaussianBlur(sharpened_image, (3, 3), 0)


def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.BICUBIC)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    temp_file.close()
    return temp_filename

def remove_noise(image):
	return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

def get_grayscale(image):
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

