import cv2
import numpy as np

def analyze_vegetation_coverage(image_bytes):
    file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if image is None:
        return 0.0, None

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    r = image_rgb[:, :, 0].astype(float)
    g = image_rgb[:, :, 1].astype(float)
    b = image_rgb[:, :, 2].astype(float)
    
    exg = 2 * g - r - b
    _, vegetation_mask = cv2.threshold(exg, 25, 255, cv2.THRESH_BINARY)
    vegetation_mask = vegetation_mask.astype(np.uint8)
    
    veg_pixels = np.count_nonzero(vegetation_mask)
    total_pixels = vegetation_mask.size
    veg_percentage = round((veg_pixels / total_pixels) * 100, 2)
    
    overlay = image_rgb.copy()
    overlay[vegetation_mask == 255] = [0, 255, 0]
    processed_preview = cv2.addWeighted(image_rgb, 0.6, overlay, 0.4, 0)
    
    return veg_percentage, processed_preview